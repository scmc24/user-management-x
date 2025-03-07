import React from 'react'
import {GridToolbarContainer,
    GridToolbarExport,GridToolbarFilterButton,
    GridToolbarQuickFilter,
} from '@mui/x-data-grid'
import { Box } from '@mui/material'


function DatagridToolbar() {
  return (
    <GridToolbarContainer sx={{display: 'flex', gap: 4, m: 1}}>
        <GridToolbarExport/>
        <GridToolbarFilterButton/>
        <GridToolbarQuickFilter/>
    </GridToolbarContainer>
  )
}

export default DatagridToolbar