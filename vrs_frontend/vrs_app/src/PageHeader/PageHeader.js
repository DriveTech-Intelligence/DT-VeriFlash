import Select from "@mui/material/Select";
import {
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";

const PageHeader = (props) => {
  const handleChange = (event) => {
    props.setProject(event.target.value);
  };

  const verifiedStat = props.vsrData?.length
    ? props.vsrData.reduce((a, v) => (a = a + v["verified"]), 0)
    : 0;
  const passedStat = props.vsrData?.length
    ? props.vsrData.reduce((a, v) => (a = a + v["passed"]), 0)
    : 0;
  const failedStat = props.vsrData?.length
    ? props.vsrData.reduce((a, v) => (a = a + v["failed"]), 0)
    : 0;

  return (
    <>
      <Grid item xs={4}>
        <FormControl sx={{ m: 1, display:'flex' }} size="small">
          <InputLabel id="project-select" >Select Project</InputLabel>
          <Select
            id="project-select"
            value={props.project.vehicle_name}
            label="Project"
            onChange={handleChange}
          >
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            {props.projectList?.length
              ? props.projectList.map((element) => (
                  <MenuItem value={element.id}>
                    {element.company_name}-{element.vehicle_name}-
                    {element.create_ts}
                  </MenuItem>
                ))
              : null}
          </Select>
        </FormControl>
      </Grid>
      <Grid item xs={8}>
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell align="center" style={{fontSize:"1.1em"}}>Total Ecus Verified</TableCell>
                <TableCell align="center" style={{fontSize:"1.1em"}}>Total Ecus Passed</TableCell>
                <TableCell align="center" style={{fontSize:"1.1em"}}>Total Ecus Failed</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow
                key="stat"
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell align="center" style={{fontSize:"1em"}}>
                  {verifiedStat}
                </TableCell>
                <TableCell align="center" style={{fontSize:"1em"}}>{passedStat}</TableCell>
                <TableCell align="center" style={{fontSize:"1em"}}>{failedStat}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>
    </>
  );
};

export default PageHeader;
