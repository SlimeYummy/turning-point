#![feature(negative_impls)]

extern crate serde;
extern crate serde_json;

mod attributes;
mod materials;
mod res_id;
mod slots;
mod table;

pub use attributes::{AttributeKey, Attributes};
pub use slots::{SlotClass, Slots};

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
