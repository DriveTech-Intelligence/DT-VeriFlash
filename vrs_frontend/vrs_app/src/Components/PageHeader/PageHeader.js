import Select from "@mui/material/Select";
import {
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import Moment from "moment";

const PageHeader = (props) => {
  const handleChange = (event) => {
    props.setProject(event.target.value);
  };

  const verifiedStat = props.vsrData?.length ? props.vsrData.length : 0;
  var failedEcus = 0;
  var passedEcus = 0;
  const passedStat = props.vsrData?.length
    ? props.vsrData.map((element) => {
        if (element["failed"] === null) {
          passedEcus = passedEcus + 1;
          return passedEcus
        }
      }) !== undefined
      ? passedEcus
      : 0
    : 0;
  const failedStat = props.vsrData?.length
    ? props.vsrData.map((element) => {
        if (element["failed"] !== null) {
          failedEcus = failedEcus + 1;
          return failedEcus
        }
      }) !== undefined
      ? failedEcus
      : 0
    : 0;

  return (
    <>
      <Grid item xs={4} padding={0}>
        <FormControl sx={{ m: 1 }} size="small" fullWidth={true}>
          <InputLabel id="project-select">Select Project</InputLabel>
          <Select
            id="project-select"
            value={props.project.vehicle_name}
            label="Select Project"
            onChange={handleChange}
            defaultValue=""
          >
            <MenuItem key="None" value="">
              <em>None</em>
            </MenuItem>
            {props.projectList?.length
              ? props.projectList.map((element) => (
                  <MenuItem key={element.id} value={element.id}>
                    {element.company_name}-{element.vehicle_name}-
                    {Moment(element.create_ts).format("MMM Do YY")}
                  </MenuItem>
                ))
              : null}
          </Select>
        </FormControl>
      </Grid>
      <Grid item xs={8}>
        <TableContainer>
          <Table
            sx={{ minWidth: 650 }}
            aria-label="simple table"
            style={{ border: "None" }}
          >
            <TableHead>
              <TableRow>
                <TableCell
                  align="center"
                  style={{ fontSize: "2em", border: "None" }}
                >
                  Total Verified
                </TableCell>
                <TableCell
                  align="center"
                  style={{ fontSize: "2em", border: "None" }}
                >
                  Total Passed
                </TableCell>
                <TableCell
                  align="center"
                  style={{ fontSize: "2em", border: "None" }}
                >
                  Total Failed
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow
                key="stat"
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell
                  align="center"
                  style={{ fontSize: "1.5em", border: "None" }}
                >
                  {verifiedStat}
                </TableCell>
                <TableCell
                  align="center"
                  style={{ fontSize: "1.5em", border: "None" }}
                >
                  {passedStat}
                </TableCell>
                <TableCell
                  align="center"
                  style={{ fontSize: "1.5em", border: "None" }}
                >
                  {failedStat}
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>
    </>
  );
};

export default PageHeader;
