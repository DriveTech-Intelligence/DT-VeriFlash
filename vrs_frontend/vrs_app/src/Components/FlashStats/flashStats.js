import { API_GET_REPORT_LIST } from "../../Data/Apiservice"
import axios from "axios";
import { useEffect, useState } from "react";
import StaticBar from "../Appbar/Appbar";
import { Grid } from "@mui/material";
import MTable from "../Table/MTable";
import PageHeader from "../PageHeader/PageHeader";
import useAuth from "../../Context/useAuth"

const FlashStats = () => {
  const [projectList, setProjectList] = useState([]);
  const [project, setProject] = useState("");
  const [vsrData, setVsrData] = useState({});
  const { auth } = useAuth();

  const getReportList = async () => {
    let response = await axios.post(API_GET_REPORT_LIST, {
      filter: auth?.company ? auth.company : "all",
    });
    let projectList = response.data;
    setProjectList(projectList);
  };

  useEffect(() => {
      getReportList();
  }, []);
  return (
    <>
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
        <MTable project={project} vsrData={vsrData} setVsrData={setVsrData} />
      </Grid>
    </>
  );
};

export default FlashStats;
