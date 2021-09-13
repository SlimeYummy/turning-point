use super::table::Table;
use anyhow::Result;
use serde::de::{self, DeserializeSeed, Deserializer, MapAccess, SeqAccess, Visitor};
use serde::Deserialize;
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Deserialize)]
pub enum SlotClass {
    Attack,
    Health,
    General,
}

pub type Slots = Table<(), SlotClass>;

impl<'de> Deserialize<'de> for Slots {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        const FIELDS: &'static [&'static str] = &["list_cnt", "list_cap", "table"];
        return deserializer.deserialize_struct("Slots", FIELDS, SlotsVisitor);
    }
}

struct SlotsVisitor;

impl<'de> Visitor<'de> for SlotsVisitor {
    type Value = Slots;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        return formatter.write_str(r#"{"list_cnt": 0, "list_cap": 0, "table": {}}"#);
    }

    fn visit_map<A: MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let mut list_cnt: u16 = 0;
        let mut list_cap: u16 = 0;
        let mut table = None;
        while let Some(key) = map.next_key()? {
            match key {
                "list_cnt" => list_cnt = map.next_value()?,
                "list_cap" => list_cap = map.next_value()?,
                "table" => {
                    if list_cnt == 0 {
                        return Err(de::Error::missing_field("list_cnt"));
                    }
                    if list_cap == 0 {
                        return Err(de::Error::missing_field("list_cap"));
                    }
                    let mut tb = Slots::new(list_cnt, list_cap);
                    map.next_value_seed(TableVisitor(&mut tb))?;
                    table = Some(tb);
                }
                _ => map.next_value()?,
            }
        }
        match table {
            Some(tb) => return Ok(tb),
            None => return Err(de::Error::missing_field("table")),
        };
    }
}

struct TableVisitor<'t>(&'t mut Slots);

impl<'de, 't> DeserializeSeed<'de> for TableVisitor<'t> {
    type Value = ();

    fn deserialize<D: Deserializer<'de>>(self, deserializer: D) -> Result<Self::Value, D::Error> {
        return deserializer.deserialize_seq(TableVisitor(self.0));
    }
}

impl<'de, 't> Visitor<'de> for TableVisitor<'t> {
    type Value = ();

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        return formatter.write_str(r#"expecting ["", ...]"#);
    }

    fn visit_seq<A: SeqAccess<'de>>(self, mut seq: A) -> Result<(), A::Error> {
        let mut idx = 0;
        while let Some(text) = seq.next_element::<&str>()? {
            let mut list = match self.0.list_mut(idx) {
                Some(list) => list,
                None => return Err(de::Error::custom("Table list_cnt overflow")),
            };
            idx += 1;

            for ch in text.chars() {
                let class = match ch {
                    'H' => SlotClass::Health,
                    'A' => SlotClass::Attack,
                    'G' => SlotClass::General,
                    _ => return Err(de::Error::custom("")),
                };
                if !list.push_item(class) {
                    return Err(de::Error::custom("Table list_cap overflow"));
                }
            }
        }
        return Ok(());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_slots_deserialize() {
        let slots: Slots = serde_json::from_str(
            r#"{
                "list_cnt": 2,
                "list_cap": 3,
                "table": ["", "AHG"]
            }"#,
        )
        .unwrap();
        assert_eq!(slots.list_cnt(), 2);
        assert_eq!(slots.list_cap(), 3);
        assert_eq!(*slots.label(0).unwrap(), ());
        assert_eq!(slots.items(0).unwrap(), &[]);
        assert_eq!(*slots.label(1).unwrap(), ());
        assert_eq!(
            slots.items(1).unwrap(),
            &[SlotClass::Attack, SlotClass::Health, SlotClass::General]
        );
    }
}
