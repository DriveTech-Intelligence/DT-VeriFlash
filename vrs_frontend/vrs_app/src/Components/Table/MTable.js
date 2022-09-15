import * as React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import { API_FETCH_FLASH_STATS } from "../../Data/Apiservice";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import "./MTable.css";
import { Box, CircularProgress } from "@mui/material";

const MTable = (props) => {
  const [showSpinner, setShowSpinner] = useState(false);
  const fetchvsrData = async () => {
    setShowSpinner(true);
    let response = await axios.post(API_FETCH_FLASH_STATS, {
      project_id: props.project,
    });
    let vsrData = response.data;
    props.setVsrData(vsrData);
    console.log(vsrData);
    setShowSpinner(false);
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
        style={{fontSize:'1em'}}
      />
    </Box>
  ) : showSpinner ? (
    <CircularProgress />
  ) : null;
};

export default MTable;
