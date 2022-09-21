import { API_GET_REPORT_LIST } from "../../Data/Apiservice";
import axios from "axios";
import { useEffect, useState, useContext } from "react";
import StaticBar from "../Appbar/Appbar";
import { Grid } from "@mui/material";
import MTable from "../Table/MTable";
import PageHeader from "../PageHeader/PageHeader";
import AuthContext from "../../Context/AuthProvider";

const FlashStats = () => {
  const [projectList, setProjectList] = useState([]);
  const [project, setProject] = useState("");
  const [vsrData, setVsrData] = useState({});
  const { auth, setAuth } = useContext(AuthContext);

  const getReportList = async () => {
    let response = await axios.post(
      API_GET_REPORT_LIST,
      {
        filter: auth?.company ? auth.company : "all",
      },
      { headers: { user_token: auth?.accessToken } }
    );
    if (response.status === 200) {
      let projectList = response.data.projectList;
      setProjectList(projectList);
      setAuth((prevState) => ({
        ...prevState,
        accessToken: response.data.token,
      }));

      if (projectList?.length === 1) {
        setProject(projectList[0].id);
      }
    }
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
