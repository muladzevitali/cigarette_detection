import React from 'react'
import axios from 'axios'
import {crawlerUrl} from "../Config";
import {Card, Table, Image, Form, Toast, Navbar, Row, Col, ListGroup, ListGroupItem} from 'react-bootstrap'
import '../Styles/ResultsTable.css'
import abbreviateNumber from '../Utils/abbreviateNumber'


class ResultsTable extends React.Component {
    constructor(props) {
        super(props);
        const modifiedData = this.props.data.map(item => {
            return item
        });
        this.state = {data: modifiedData}
    }

    render() {
        return (
            <div>
                <Card className="resultsCard">
                    <Row>
                        <Card style={{width: '18rem'}} bg='secondary' className='resultsMainCard'>
                            <Card.Img variant="top" src="/output.jpg" className='cigaretteImage'/>
                            <ListGroup className="list-group-flush">
                                <ListGroupItem variant='dark'>Found cigarettes: 63</ListGroupItem>
                            </ListGroup>
                        </Card>

                        <Card style={{width: '18rem'}} bg='secondary' className='resultsMainCard'>
                            <Card.Img variant="top" src="/output.jpg" className='cigaretteImage'/>
                            <ListGroup className="list-group-flush">
                                <ListGroupItem variant='dark'>Company: Malboro</ListGroupItem>
                                <ListGroupItem variant='dark'>Found cigarettes: 63</ListGroupItem>
                                <ListGroupItem variant='dark'>Found cigarettes: 63</ListGroupItem>
                            </ListGroup>
                        </Card>
                    </Row>

                </Card>
            </div>
        );
    }
}

export default ResultsTable;