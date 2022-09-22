import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import DTLogo from '../../assets/DriveTechLogo.svg'

export default function StaticBar() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar variant="dense">
          <img alt='logo' src={DTLogo} style={{height:'1em'}}/>
          <Typography sx={{ml:'0.5em'}} variant="h6" color="inherit" component="div">
            Vehicle Scan Report Summary
          </Typography>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
