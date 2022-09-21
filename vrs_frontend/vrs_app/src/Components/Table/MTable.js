import * as React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import { API_FETCH_FLASH_STATS } from "../../Data/Apiservice";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import "./MTable.css";
import { Box, CircularProgress, Typography, Tooltip } from "@mui/material";
import AuthContext from "../../Context/AuthProvider";

const MTable = (props) => {
  const [showSpinner, setShowSpinner] = useState(false);
  const [error, setError] = useState(null);
  const { auth, setAuth } = React.useContext(AuthContext);

  const fetchvsrData = async () => {
    setShowSpinner(true);
    try {
      let response = await axios.post(
        API_FETCH_FLASH_STATS,
        {
          project_id: props.project,
        },
        { headers: { user_token: auth?.accessToken } }
      );
      if (response.status === 200) {
        let vsrData = response.data.flashStats;
        props.setVsrData(vsrData);
        setShowSpinner(false);
        setAuth((prevState) => ({
          ...prevState,
          accessToken: response.data.token,
        }));
      }
    } catch (error) {
      console.log(error);
      setShowSpinner(false);
      setError(error.response.data.detail);
    }
  };

  const createColumns = (vsrData) => {
    const columns = [];
    Object.keys(vsrData[0]).forEach((element) => {
      columns.push({
        field: element,
        headerName:
          element === "id"
            ? "VIN"
            : element === "verified"
            ? "VERIFIED ECUS"
            : element === "failed"
            ? "FAILED ECUS"
            : element === "passed"
            ? "PASSED ECUS"
            : element === "failed_ecus"
            ? "FAILED ECU NAMES"
            : element === "incorrectly_flashed"
            ? "INCORRECTLY FLASHED"
            : element === "vin_mismatch"
            ? "VIN MISMATCH"
            : element.toUpperCase(),
        type:
          element === "failed"
            ? "number"
            : element === "passed"
            ? "number"
            : element === "verified"
            ? "number"
            : "string",
        align: "center",
        headerAlign: "center",
        headerClassName: "mtable",
        width:
          element === "filename"
            ? 700
            : (element === "verified") |
              (element === "passed") |
              (element === "failed")
            ? 100
            : 209,
        renderCell:
          element === "filename" || element === "failed_ecus"
            ? (params) => (
                <Tooltip title={params.formattedValue}>
                  <span className="table-cell-trucate">
                    {params.formattedValue}
                  </span>
                </Tooltip>
              )
            : null,
      });
    });
    return columns;
  };

  const createRows = (vsrData) => {
    const rows = vsrData;
    return rows;
  };

  useEffect(() => {
    if (Object.keys(props.project).length !== 0) {
      fetchvsrData();
    }
  }, [props.project]);

  return props.vsrData?.length && !showSpinner ? (
    <Box
      sx={{
        height: 700,
        width: "100%",
        "& .error": {
          color: "red",
        },
      }}
    >
      <DataGrid
        rows={createRows(props.vsrData)}
        columns={createColumns(props.vsrData)}
        components={{ Toolbar: GridToolbar }}
        hideFooterPagination={true}
        hideFooter={true}
        disableSelectionOnClick={true}
        getCellClassName={(params) => {
          if (params.field === "vin_mismatch" && params.value === "Mismatch") {
            return "error";
          }
          if (params.field === "failed_ecus" && params.value !== "") {
            return "error";
          }
          if (params.field === "incorrectly_flashed" && params.value !== null) {
            return "error";
          }
        }}
        style={{ fontSize: "1em" }}
        initialState={{
          sorting: {
            sortModel: [{ field: "failed", sort: "desc" }],
          },
        }}
      />
    </Box>
  ) : showSpinner ? (
    <div
      style={{
        marginLeft: "auto",
        marginRight: "auto",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <CircularProgress style={{ marginLeft: "auto", marginRight: "auto" }} />
      <span style={{ fontSize: "0.7em" }}>
        Vehicle Scan Reports are being processed...
      </span>
    </div>
  ) : error !== null && !showSpinner ? (
    <div
      style={{
        marginLeft: "auto",
        marginRight: "auto",
      }}
    >
      <Typography component="h3" variant="h7">
        {error}
      </Typography>
    </div>
  ) : null;
};

export default MTable;
