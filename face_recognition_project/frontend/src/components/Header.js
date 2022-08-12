import React from 'react'
import { Navbar, Nav, Container, Row, NavDropdown } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import {useDispatch,useSelector} from 'react-redux'
import {logout} from '../actions/userActions'

function Header() {
    const userLogin = useSelector(state => state.userLogin)
    const {userInfo} = userLogin

    const dispatch = useDispatch()

    const logoutHandler=()=>{
        dispatch(logout())
    }
    return (
        <div>
            <header>
            <Navbar bg="light" expand="lg">
            <Container>
                <LinkContainer to='/'>
                    <Navbar.Brand >MIHAEL SHOP</Navbar.Brand>
                </LinkContainer>
                
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ms-auto">
                    <LinkContainer to='/cart' >
                        <Nav.Link>Cart</Nav.Link>
                    </LinkContainer>

                    {userInfo && userInfo.isAdmin && (
                        <NavDropdown title='Admin' id='adminmenue' >
                            <LinkContainer to='/users/'>
                                <NavDropdown.Item>Users</NavDropdown.Item>
                            </LinkContainer>

                            <LinkContainer to='/productlist'>
                                <NavDropdown.Item>Products</NavDropdown.Item>
                            </LinkContainer>

                            <LinkContainer to='/orderlist'>
                                <NavDropdown.Item>Orders</NavDropdown.Item>
                            </LinkContainer>

                        </NavDropdown>
                    )}

                    {userInfo ? (
                            <NavDropdown title={userInfo.name} id='username'>
                                <Container>
                                    <LinkContainer to='/profile'>
                                        <NavDropdown.Item>
                                            Profile
                                        </NavDropdown.Item>
                                    </LinkContainer>
                                </Container>

                                <Container onClick={logoutHandler}>
                                    <NavDropdown.Item>
                                        Logout
                                    </NavDropdown.Item>
                                </Container>
                            </NavDropdown>
                        ):(
                            <LinkContainer to='/login'>
                                <Nav.Link>Login</Nav.Link> 
                            </LinkContainer>  
                        )}   
                </Nav>
                </Navbar.Collapse>
            </Container>
            </Navbar>
            </header>
        </div>
    );
}

export default Header