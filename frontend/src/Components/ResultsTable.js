import React from 'react'
import {Card, Col, Form, ListGroup, ListGroupItem, Row} from 'react-bootstrap'
import '../Styles/ResultsTable.css'


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
                        <Card className='resultsMainCard' style={{height: 'auto'}}>
                            <Card.Img variant="top" src="/output.jpg" className='cigaretteImage'/>
                            <ListGroup className="list-group-flush">
                                <ListGroupItem className='resultsListItem'>
                                    <Row>
                                    <Col className='nameTarget'>
                                        Found 63 packs of cigarette
                                    </Col>

                                </Row></ListGroupItem>
                            </ListGroup>
                        </Card>

                        <Card className='resultsMainCard'>
                            <Card.Img variant="top" src="/output.jpg" className='cigaretteImage'/>
                            <ListGroup className="list-group-flush">
                                <ListGroupItem className='resultsListItem'>
                                    <Row>
                                        <Col className='nameTarget'>
                                            Company:
                                        </Col>
                                        <Col>
                                            <Form>
                                                <div className='companyName'>
                                                    <Form.Control aria-label="Word"
                                                                  className='companyNameInput'
                                                                  name='companyName'
                                                                  type="text"
                                                                  autoFocus
                                                                  value='Malboro'
                                                    />
                                                </div>
                                            </Form>
                                        </Col>
                                    </Row>
                                </ListGroupItem>
                                <ListGroupItem className='resultsListItem'>
                                    <Row>
                                        <Col className='nameTarget'>
                                            Precision:
                                        </Col>
                                        <Col>
                                            0.8
                                        </Col>
                                    </Row>
                                </ListGroupItem>
                                <ListGroupItem className='resultsListItem'>
                                    <Row>
                                        <Col className='nameTarget'>
                                            Top point:
                                        </Col>
                                        <Col>
                                            (3, 4)
                                        </Col>
                                    </Row>
                                </ListGroupItem>
                                <ListGroupItem className='resultsListItem'>
                                    <Row>
                                        <Col className='nameTarget'>
                                            Bottom point:
                                        </Col>
                                        <Col>
                                            (3, 4)
                                        </Col>
                                    </Row>
                                </ListGroupItem>
                            </ListGroup>
                        </Card>
                    </Row>

                </Card>
            </div>
        );
    }
}

export default ResultsTable;