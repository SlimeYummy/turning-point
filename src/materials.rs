use super::table::{ListMut, Table};
use anyhow::Result;
use serde::de::{self, DeserializeSeed, Deserializer, MapAccess, SeqAccess, Visitor};
use serde::Deserialize;
use std::fmt;
use ustr::Ustr;

pub type Materials = Table<(), (Ustr, f64)>;

impl<'de> Deserialize<'de> for Materials {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        const FIELDS: &'static [&'static str] = &["list_cnt", "list_cap", "table"];
        return deserializer.deserialize_struct("Materials", FIELDS, VariablesVisitor);
    }
}

struct VariablesVisitor;

impl<'de> Visitor<'de> for VariablesVisitor {
    type Value = Materials;

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
                    let mut tb = Materials::new(list_cnt, list_cap);
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

struct TableVisitor<'t>(&'t mut Materials);

impl<'de, 't> DeserializeSeed<'de> for TableVisitor<'t> {
    type Value = ();

    fn deserialize<D: Deserializer<'de>>(self, deserializer: D) -> Result<Self::Value, D::Error> {
        return deserializer.deserialize_seq(TableVisitor(self.0));
    }
}

impl<'de, 't> Visitor<'de> for TableVisitor<'t> {
    type Value = ();

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        return formatter.write_str(r#"expecting [[], ...]"#);
    }

    fn visit_seq<A: SeqAccess<'de>>(self, mut seq: A) -> Result<(), A::Error> {
        let mut idx = 0;
        loop {
            let list = match self.0.list_mut(idx) {
                Some(list) => list,
                None => break,
            };
            idx += 1;
            let _ = seq.next_element_seed(ListVisitor(list))?;
        }
        if seq.next_element::<Vec<f64>>()?.is_some() {
            return Err(de::Error::custom("Table list_cnt overflow"));
        }
        return Ok(());
    }
}

struct ListVisitor<'t>(ListMut<'t, (), (Ustr, f64)>);

impl<'de, 't> DeserializeSeed<'de> for ListVisitor<'t> {
    type Value = ();

    fn deserialize<D: Deserializer<'de>>(self, deserializer: D) -> Result<Self::Value, D::Error> {
        return deserializer.deserialize_map(ListVisitor(self.0));
    }
}

impl<'de, 't> Visitor<'de> for ListVisitor<'t> {
    type Value = ();

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        return formatter.write_str(r#"expecting [Fx64, ...]"#);
    }

    fn visit_map<A: MapAccess<'de>>(mut self, mut map: A) -> Result<Self::Value, A::Error> {
        while let Some(entry) = map.next_entry()? {
            if !self.0.push_item(entry) {
                return Err(de::Error::custom("Table list_cap overflow"));
            }
        }
        return Ok(());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_materials_deserialize() {
        let vars: Materials = serde_json::from_str(
            r#"{
                "list_cnt": 2,
                "list_cap": 3,
                "table": [
                    {"Material.1": 1, "Material.2": 2},
                    {"Material.1": 1, "Material.2": 2, "Material.3": 3}
                ]
            }"#,
        )
        .unwrap();
        assert_eq!(vars.list_cnt(), 2);
        assert_eq!(vars.list_cap(), 3);
        assert_eq!(*vars.label(0).unwrap(), ());
        assert_eq!(
            vars.items(0).unwrap(),
            &[
                (Ustr::from("Material.1"), 1.0),
                (Ustr::from("Material.2"), 2.0)
            ]
        );
        assert_eq!(*vars.label(1).unwrap(), ());
        assert_eq!(
            vars.items(1).unwrap(),
            &[
                (Ustr::from("Material.1"), 1.0),
                (Ustr::from("Material.2"), 2.0),
                (Ustr::from("Material.3"), 3.0)
            ]
        );
    }
}
