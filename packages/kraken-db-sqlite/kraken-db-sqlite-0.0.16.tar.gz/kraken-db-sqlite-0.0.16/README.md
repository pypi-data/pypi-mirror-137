Library to schema_org


## How to use
`from kraken_db import kraken_db as db`

`db.init()`

## Data dictionary
### Observation
    id = Column(String)
    observation_id = Column(String, primary_key=True)
    ref_id = Column(String)
    datasource = Column(String)
    agent = Column(String)
    instrument = Column(String)
    object = Column(String)
    result = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    valid = Column(Boolean)

    record_type = Column(String)
    record_id = Column(String)
    key = Column(String)
    value = Column(String)
    credibility = Column(Float)
    created_date = Column(DateTime)    