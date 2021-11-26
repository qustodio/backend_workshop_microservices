import { Drawer, Divider, List, ListItem, ListItemIcon, ListItemText, Container } from "@mui/material";
import {
  Home as HomeIcon,
  LibraryBooks as LibraryBooksIcon,
  People as PeopleIcon,
  Login as LoginIcon,
} from '@mui/icons-material';
import { Box } from '@mui/system';
import { Link } from 'react-router-dom';
import { useAuth } from "../../lib/auth";

const drawerWidth = 240;

type MenuItem = {
  icon: JSX.Element;
  label: string;
  link: string;
}

type Menu = MenuItem[];

const menuTop = [
  {
    icon: <HomeIcon />,
    label: 'Home',
    link: '/'
  },
  {
    icon: <LibraryBooksIcon />,
    label: 'Books',
    link: '/books'
  },
  {
    icon: <PeopleIcon />,
    label: 'Authors',
    link: '/authors'
  }
];

const menuLogin = [
  {
    icon: <LoginIcon />,
    label: 'Login',
    link: '/login'
  }
];

const menuUserLogged = [
  {
    icon: <LibraryBooksIcon />,
    label: 'My loans',
    link: '/loans'
  }
];

const Layout = ({children}: {children: JSX.Element}) =>
  <Box sx={{ display: 'flex' }}>
    <Menu />
    <Box
      component="main"
      sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}
    >
      <Container>
        {children}
      </Container>
    </Box>
  </Box>

const Menu = () => {
  const { user } = useAuth();

  const renderMenu = (menu: Menu) => (
    menu.map((item, index) => (
      <Link to={item.link} >
        <ListItem button key={item.label}>
          <ListItemIcon>
            {item.icon}
          </ListItemIcon>
          <ListItemText primary={item.label} />
        </ListItem>
      </Link>
    ))
  );

  return (
    <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        aria-label="mailbox folders"
    >
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        variant="permanent"
        anchor="left"
      >
        <List>
          {renderMenu(menuTop)}
        </List>
        <Divider />
        <List>
          {user ? renderMenu(menuUserLogged) : renderMenu(menuLogin)}
        </List>
      </Drawer>
    </Box>
  );
}

export default Layout;
