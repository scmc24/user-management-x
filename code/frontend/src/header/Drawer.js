import * as React from 'react';
import {
  Box,
  Drawer,
  List,
  Divider,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
} from '@mui/material';
import { Link } from 'react-router-dom';
import HomeIcon from '@mui/icons-material/Home';
import ManageAccountsIcon from '@mui/icons-material/ManageAccounts';
import PeopleIcon from '@mui/icons-material/People';
import { useSelector } from 'react-redux';

function MyDrawer({ open, toggleDrawer }) {
  const isAdmin = useSelector((state) => state.isAdmin);
  const isLoggedIn = useSelector((state) => state.isLoggedIn);

  // Common navigation items
  const icons = [
    { name: 'Home', icon: <HomeIcon />, route: '/' },
  ];

  // Logged-in user navigation items
  const loggedInIcons = [
    { name: 'Profile', icon: <ManageAccountsIcon />, route: '/profile' },
  ];

  // Admin-specific navigation items
  const adminIcons = [
    { name: 'Users', icon: <PeopleIcon />, route: '/clients' },
  ];

  const DrawerList = (
    <Box sx={{ width: 250 }} role="presentation" onClick={toggleDrawer(false)}>
      {/* App Name or Logo */}
      <Typography
        variant="h6"
        sx={{
          p: 2,
          textAlign: 'center',
          fontWeight: 'bold',
          color: 'primary.main',
        }}
      >
        Account Management Microservice
      </Typography>

      {/* Common Navigation Items */}
      <List>
        {icons.map((item, index) => (
          <ListItem key={index} disablePadding>
            <ListItemButton
              component={Link}
              to={item.route}
              sx={{
                '&:hover': {
                  backgroundColor: 'primary.light',
                },
              }}
            >
              <ListItemIcon sx={{ color: 'primary.main' }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText
                primary={item.name}
                primaryTypographyProps={{ fontWeight: 'medium' }}
              />
            </ListItemButton>
          </ListItem>
        ))}
        {isLoggedIn &&
          loggedInIcons.map((item, index) => (
            <ListItem key={index} disablePadding>
              <ListItemButton
                component={Link}
                to={item.route}
                sx={{
                  '&:hover': {
                    backgroundColor: 'primary.light',
                  },
                }}
              >
                <ListItemIcon sx={{ color: 'primary.main' }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.name}
                  primaryTypographyProps={{ fontWeight: 'medium' }}
                />
              </ListItemButton>
            </ListItem>
          ))}
      </List>

      {/* Admin Navigation Items (Conditional) */}
      {isAdmin && (
        <>
          <Divider sx={{ my: 1 }} />
          <Typography
            variant="subtitle2"
            sx={{ px: 2, py: 1, color: 'text.secondary' }}
          >
            Admin Tools
          </Typography>
          <List>
            {adminIcons.map((item, index) => (
              <ListItem key={index} disablePadding>
                <ListItemButton
                  component={Link}
                  to={item.route}
                  sx={{
                    '&:hover': {
                      backgroundColor: 'secondary.light',
                    },
                  }}
                >
                  <ListItemIcon sx={{ color: 'secondary.main' }}>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText
                    primary={item.name}
                    primaryTypographyProps={{ fontWeight: 'medium' }}
                  />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </>
      )}
    </Box>
  );

  return (
    <Drawer open={open} onClose={toggleDrawer(false)}>
      {DrawerList}
    </Drawer>
  );
}

export default MyDrawer;