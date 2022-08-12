import React from 'react'
import Row from 'react-bootstrap/Row'
import Container from 'react-bootstrap/Container'
import Col from 'react-bootstrap/Col'

function Footer() {
    return (
        <footer>
            <Container>
                <Row>
                    <Col className = "text-center py-3" >Copyright</Col>
                </Row>
            </Container>
        </footer>
    );
}

export default Footer