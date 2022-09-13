import "./App.css";
import StaticBar from "./Appbar/Appbar";
import { useEffect, useState } from "react";
import { Grid } from "@mui/material";
import MTable from "./Table/MTable";
import PageHeader from "./PageHeader/PageHeader";
import { API_GET_REPORT_LIST } from "./Data/Apiservice";
import axios from "axios";

function App() {
  const [projectList, setProjectList] = useState([]);
  const [project, setProject] = useState("");
  const [vsrData, setVsrData] = useState({});

  const getReportList = async () => {
    let response = await axios.post(API_GET_REPORT_LIST, {
      company_name: "MRV",
    });
    let projectList = response.data;
    setProjectList(projectList);
  };

  useEffect(() => {
    if (!projectList?.length) {
      getReportList();
    }
  }, [projectList]);

  return (
    <div className="App">
      <header className="App-header">
        <StaticBar></StaticBar>
      </header>
      <Grid container spacing={2} padding={5}>
        <PageHeader
          project={project}
          projectList={projectList}
          setProject={setProject}
          vsrData={vsrData}
        />
      </Grid>
      <Grid container paddingLeft={5} paddingRight={5}>
        <MTable project={project} vsrData={vsrData} setVsrData={setVsrData}/>
      </Grid>
    </div>
  );
}

export default App;
