import React from 'react'
import {Card, Col, Form, ListGroup, ListGroupItem, Modal, Row} from 'react-bootstrap'
import '../Styles/ResultsTable.css'


class ResultsTable extends React.Component {
    constructor(props) {
        super(props);
        const modifiedData = this.props.data.map(item => {
            return item
        });
        this.state = {
            data: modifiedData,
            showModal: false,
            modalImagePath: null
        }
    }

    showModal = imagePath => event => {
        this.setState({showModal: true, modalImagePath: imagePath})
    }

    render() {
        return (
            <div>
                <Card className="resultsMainCard">
                    <Row>
                        <Card className='resultsSmallCard' style={{height: 'auto'}}>
                            <Card.Img variant="top" src="/output.jpg"
                                      className='cigaretteImage'
                                      onClick={this.showModal('/output.jpg')}/>
                            <ListGroup className="list-group-flush">
                                <ListGroupItem className='resultsListItem'>
                                    <Row>
                                        <Col className='nameTarget'>
                                            Found 63 packs of cigarette
                                        </Col>

                                    </Row></ListGroupItem>
                            </ListGroup>
                        </Card>

                        <Card className='resultsSmallCard'>
                            <Card.Img variant="top" src="/output.jpg"
                                      className='cigaretteImage'
                                      onClick={this.showModal('/output.jpg')}/>
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
                                                                  defaultValue='Malboro'
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

                            </ListGroup>
                        </Card>
                    </Row>

                </Card>
                <ImageModal
                    show={this.state.showModal}
                    image_path={this.state.modalImagePath}
                    onHide={() => this.setState({showModal: false})}
                />
            </div>
        );
    }
}

function ImageModal(props) {
    const {image_path} = {...props}
    return (
        <Modal
            {...props}
            size="sm"
            aria-labelledby="contained-modal-title-vcenter"
            centered
            className='imageModal'
        >
            <Modal.Body style={{backgroundColor: 'transparent'}}>
                <img
                    src={image_path}
                    className="d-inline-block align-top"
                    alt="cigaretteLogo"
                />
            </Modal.Body>

        </Modal>
    );
}


export default ResultsTable;