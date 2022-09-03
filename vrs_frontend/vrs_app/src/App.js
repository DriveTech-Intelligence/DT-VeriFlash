import './App.css';
import StaticBar from "./Appbar/Appbar"
import "./App.css";
import {
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Typography,
} from "@mui/material";
import MTable from "./Table/MTable";
import { useState } from "react";
import Select from "@mui/material/Select";

function App() {
  const [ecu, setEcu] = useState("");

  const handleChange = (event) => {
    setEcu(event.target.value);
  };
  return (
    <div className="App">
      <header className="App-header">
        <StaticBar></StaticBar>
      </header>
      <Grid container spacing={2} padding={5}>
        <Grid item xs={4}>
          <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
            <InputLabel id="ecu-select">ECU</InputLabel>
            <Select
              labelId="ecu-select"
              id="ecu-select"
              value={ecu}
              label="Ecu"
              onChange={handleChange}
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              <MenuItem value={10}>PCM</MenuItem>
              <MenuItem value={20}>Radio</MenuItem>
              <MenuItem value={30}>TCM</MenuItem>
              <MenuItem value={40}>SCRM</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={8}>
          <Typography>Statistics</Typography>
        </Grid>
      </Grid>
      <Grid container padding={5}>
        <MTable />
      </Grid>
    </div>
  );
}

export default App;
