use super::table::{ListMut, Table};
use anyhow::Result;
use serde::de::{self, DeserializeSeed, Deserializer, MapAccess, SeqAccess, Visitor};
use serde::Deserialize;
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum AttributeKey {
    MaxHealth,
    HealthCureRatio,
    Attack,
    AttackUp,
    PhyAttack,
    PhyAttackUp,
    ElmAttack,
    ElmAttackUp,
    SpeAttack,
    SpeAttackUp,
    Defense,
    DefenseUp,
    PhyDefense,
    PhyDefenseUp,
    ElmDefense,
    ElmDefenseUp,
    SpeDefense,
    EpeDefenseUp,
    CritChanceRatio,
    CritDamageRatio,
    MaxShield,
    ShieldSpeed,
    PhyBreakUp,
    ElmBreakUp,
    SpeBreakUp,
}

pub type Attributes = Table<AttributeKey, f32>;

impl<'de> Deserialize<'de> for Attributes {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        const FIELDS: &'static [&'static str] = &["list_cnt", "list_cap", "table"];
        return deserializer.deserialize_struct("Attributes", FIELDS, AttributesVisitor);
    }
}

struct AttributesVisitor;

impl<'de> Visitor<'de> for AttributesVisitor {
    type Value = Attributes;

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
                    let mut tb = Attributes::new(list_cnt, list_cap);
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

struct TableVisitor<'t>(&'t mut Attributes);

impl<'de, 't> DeserializeSeed<'de> for TableVisitor<'t> {
    type Value = ();

    fn deserialize<D: Deserializer<'de>>(self, deserializer: D) -> Result<Self::Value, D::Error> {
        return deserializer.deserialize_map(TableVisitor(self.0));
    }
}

impl<'de, 't> Visitor<'de> for TableVisitor<'t> {
    type Value = ();

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        return formatter.write_str(r#"expecting {"..": [], ...}"#);
    }

    fn visit_map<A: MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let mut idx = 0;
        while let Some(key) = map.next_key()? {
            let mut list = match self.0.list_mut(idx) {
                Some(list) => list,
                None => return Err(de::Error::custom("Table list_cnt overflow")),
            };
            idx += 1;

            list.set_label(key);
            map.next_value_seed(ListVisitor(list))?;
        }
        return Ok(());
    }
}

struct ListVisitor<'t>(ListMut<'t, AttributeKey, f32>);

impl<'de, 't> DeserializeSeed<'de> for ListVisitor<'t> {
    type Value = ();

    fn deserialize<D: Deserializer<'de>>(self, deserializer: D) -> Result<Self::Value, D::Error> {
        return deserializer.deserialize_seq(ListVisitor(self.0));
    }
}

impl<'de, 't> Visitor<'de> for ListVisitor<'t> {
    type Value = ();

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        return formatter.write_str(r#"expecting [Fx32, ...]"#);
    }

    fn visit_seq<A: SeqAccess<'de>>(mut self, mut seq: A) -> Result<(), A::Error> {
        while let Some(elem) = seq.next_element()? {
            if !self.0.push_item(elem) {
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
    fn test_attributes_deserialize() {
        let attrs: Attributes = serde_json::from_str(
            r#"{
                "list_cnt": 2,
                "list_cap": 5,
                "table": {
                    "max_health": [100,200,300,400,500],
                    "max_shield": [20,40,60,80,100]
                }
            }"#,
        )
        .unwrap();
        assert_eq!(attrs.list_cnt(), 2);
        assert_eq!(attrs.list_cap(), 5);
        assert_eq!(*attrs.label(0).unwrap(), AttributeKey::MaxHealth);
        assert_eq!(
            attrs.items(0).unwrap(),
            &[100.0, 200.0, 300.0, 400.0, 500.0]
        );
        assert_eq!(*attrs.label(1).unwrap(), AttributeKey::MaxShield);
        assert_eq!(attrs.items(1).unwrap(), &[20.0, 40.0, 60.0, 80.0, 100.0]);
    }
}
