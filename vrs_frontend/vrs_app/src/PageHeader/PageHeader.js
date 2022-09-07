import Select from "@mui/material/Select";
import { FormControl, InputLabel, MenuItem } from "@mui/material";

const PageHeader = (props) => {
  const handleChange = (event) => {
    props.setProject(event.target.value);
  };

  return (
    <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
      <InputLabel id="project-select">Project</InputLabel>
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
              <MenuItem value={element.id}>{element.vehicle_name}</MenuItem>
            ))
          : null}
      </Select>
    </FormControl>
  );
};

export default PageHeader;
