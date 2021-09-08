use std::fmt::{self, Debug, Formatter};
use std::marker::PhantomData;
use std::mem;
use std::ptr;
use std::slice;

pub struct Table<L, I>
where
    L: Copy,
    I: Copy,
{
    list_cnt: u16,
    list_cap: u16,
    list_size: u32,
    buffer: Vec<u8>,
    phantom: PhantomData<(L, I)>,
}

impl<L, I> Table<L, I>
where
    L: Copy,
    I: Copy,
{
    pub fn new(list_cnt: u16, list_cap: u16) -> Table<L, I> {
        let list_size = List::<L, I>::size(list_cap);
        let buffer_size = (list_cnt as usize) * list_size;
        return Table {
            list_cnt,
            list_cap,
            list_size: list_size as u32,
            buffer: vec![0; buffer_size],
            phantom: PhantomData,
        };
    }

    pub fn list_cnt(&self) -> u16 {
        return self.list_cnt;
    }

    pub fn list_cap(&self) -> u16 {
        return self.list_cap;
    }

    pub fn label<'t>(&'t self, idx: u16) -> Option<&'t L> {
        let list = self.list_ref(idx)?;
        return Some(list.label());
    }

    pub fn items<'t>(&'t self, idx: u16) -> Option<&'t [I]> {
        let list = self.list_ref(idx)?;
        return Some(list.items());
    }

    pub fn pair<'t>(&'t self, idx: u16) -> Option<(&'t L, &'t [I])> {
        let list = self.list_ref(idx)?;
        return Some((list.label(), list.items()));
    }

    pub(crate) fn list_ref<'t>(&'t self, idx: u16) -> Option<ListRef<'t, L, I>> {
        if idx >= self.list_cnt {
            return None;
        }
        let offset = (self.list_size as usize) * (idx as usize);
        unsafe {
            let ptr = &self.buffer[offset] as *const _ as *const List<L, I>;
            return Some(ListRef { list: &*ptr });
        }
    }

    pub(crate) fn list_mut<'t>(&'t mut self, idx: u16) -> Option<ListMut<'t, L, I>> {
        if idx >= self.list_cnt {
            return None;
        }
        let offset = (self.list_size as usize) * (idx as usize);
        unsafe {
            let ptr = &mut self.buffer[offset] as *mut _ as *mut List<L, I>;
            return Some(ListMut {
                cap: self.list_cap,
                list: &mut *ptr,
            });
        }
    }
}

impl<L, I> Debug for Table<L, I>
where
    L: Copy + Debug,
    I: Copy + Debug,
{
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        let mut map = f.debug_map();
        for idx in 0..self.list_cnt {
            if let Some((label, items)) = self.pair(idx) {
                map.entry(label, &items);
            }
        }
        return map.finish();
    }
}

#[repr(C)]
struct List<L, I>
where
    L: Copy,
    I: Copy,
{
    label: L,
    len: u16,
    items: [I; 1],
}

impl<L, I> List<L, I>
where
    L: Copy,
    I: Copy,
{
    fn size(len: u16) -> usize {
        let ptr_self: *const Self = ptr::null();
        let item_offset = unsafe { &(*ptr_self).items } as *const [I; 1] as usize;

        let aligned_unit = usize::max(
            mem::align_of::<u16>(),
            usize::max(mem::align_of::<L>(), mem::align_of::<I>()),
        );

        let unaligned_size = item_offset + mem::size_of::<I>() * (len as usize);
        if aligned_unit == 0 {
            return unaligned_size;
        } else {
            return (unaligned_size + aligned_unit - 1) / aligned_unit * aligned_unit;
        }
    }
}

pub(crate) struct ListRef<'t, L, I>
where
    L: Copy,
    I: Copy,
{
    list: &'t List<L, I>,
}

impl<'t, L, I> ListRef<'t, L, I>
where
    L: Copy,
    I: Copy,
{
    pub(crate) fn len(&self) -> u16 {
        return self.list.len;
    }

    pub(crate) fn label(&self) -> &'t L {
        return &self.list.label;
    }

    pub(crate) fn items(&self) -> &'t [I] {
        let data = self.list.items.as_ptr();
        let len = self.len() as usize;
        return unsafe { slice::from_raw_parts(data, len) };
    }
}

pub(crate) struct ListMut<'t, L, I>
where
    L: Copy,
    I: Copy,
{
    cap: u16,
    list: &'t mut List<L, I>,
}

impl<'t, L, I> ListMut<'t, L, I>
where
    L: Copy,
    I: Copy,
{
    pub(crate) fn cap(&self) -> u16 {
        return self.cap;
    }

    pub(crate) fn len(&self) -> u16 {
        return self.list.len;
    }

    pub(crate) fn set_label(&mut self, label: L) {
        self.list.label = label;
    }

    pub(crate) fn push_item(&mut self, item: I) -> bool {
        if self.cap() <= self.len() {
            return false;
        }
        unsafe {
            let pointer = self.list.items.as_mut_ptr();
            ptr::write(pointer.offset(self.len() as isize), item);
        };
        self.list.len += 1;
        return true;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_table_list_size() {
        assert_eq!(List::<(), ()>::size(1), 2);
        assert_eq!(List::<(), ()>::size(9), 2);

        assert_eq!(List::<(), u8>::size(1), 4);
        assert_eq!(List::<(), u8>::size(8), 10);
        assert_eq!(List::<(), u8>::size(9), 12);

        assert_eq!(List::<u8, u8>::size(1), 6);
        assert_eq!(List::<u8, u8>::size(8), 12);

        assert_eq!(List::<(u8, u8, u8), u8>::size(1), 8);
        assert_eq!(List::<(u8, u8, u8), u8>::size(8), 14);
        assert_eq!(List::<(u8, u8, u8), ()>::size(8), 6);

        assert_eq!(List::<(u8, u8, u8, u8, u8), u8>::size(1), 10);
        assert_eq!(List::<(u8, u8, u8, u8, u8), u8>::size(8), 16);

        assert_eq!(List::<(u16, u8, u8, u8), u8>::size(1), 10);
        assert_eq!(List::<(u16, u8, u8, u8), u8>::size(7), 16);

        assert_eq!(List::<u32, u16>::size(1), 8);
        assert_eq!(List::<u32, u16>::size(3), 12);
        assert_eq!(List::<u32, u16>::size(4), 16);

        assert_eq!(List::<u32, u64>::size(1), 16);
        assert_eq!(List::<u32, u64>::size(2), 24);
        assert_eq!(List::<u32, u64>::size(3), 32);

        assert_eq!(List::<u32, (u8, u8, u8)>::size(1), 12);
        assert_eq!(List::<u32, (u8, u8, u8)>::size(2), 12);
        assert_eq!(List::<u32, (u8, u8, u8)>::size(3), 16);
        assert_eq!(List::<u32, (u8, u8, u8)>::size(4), 20);
    }

    #[test]
    fn test_table_table() {
        let mut table = Table::<u8, f32>::new(3, 4);
        assert_eq!(table.list_cnt(), 3);
        assert_eq!(table.list_cap(), 4);
        assert_eq!(table.list_size, 20);
        assert_eq!(table.buffer.len(), 3 * 20);

        assert_eq!(
            table.list_ref(0).unwrap().list as *const _ as usize,
            table.buffer.as_ptr() as usize,
        );
        assert_eq!(
            table.list_mut(2).unwrap().list as *const _ as usize,
            table.buffer.as_ptr() as usize + 20 * 2,
        );
        assert!(table.list_mut(10).is_none());
    }

    #[test]
    fn test_table_list() {
        let mut table = Table::<u8, f32>::new(3, 2);
        {
            let mut list = table.list_mut(2).unwrap();
            assert_eq!(list.cap(), 2);
            assert_eq!(list.len(), 0);
            list.set_label(123);
            assert_eq!(list.push_item(10.0), true);
            assert_eq!(list.push_item(20.0), true);
            assert_eq!(list.push_item(30.0), false);
        }
        {
            let list = table.list_ref(2).unwrap();
            assert_eq!(list.len(), 2);
            assert_eq!(*list.label(), 123);
            assert_eq!(list.items(), &[10.0, 20.0]);
        }
    }
}
