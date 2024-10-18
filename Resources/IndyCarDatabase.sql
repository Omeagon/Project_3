DROP TABLE IF EXISTS indydata_2024;

CREATE TABLE indydata_2024 ( 
  race_num INTEGER,
  race_city TEXT,
  rank INTEGER,
  driver VARCHAR(30),
  car_no INTEGER,
  start INTEGER,
  laps INTEGER,
  total_time DECIMAL,
  laps_led INT,
  status VARCHAR(30),
  avg_speed REAL,
  num_pit_stop INTEGER,
  points INTEGER,
  points_f1 INTEGER,
  points_IMSA INTEGER,
  track_type VARCHAR(30),
  PRIMARY KEY (race_num, rank) -- COMPOSITE KEY
);