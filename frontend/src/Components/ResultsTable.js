import React from 'react'
import {Card, Col, Form, ListGroup, ListGroupItem, Modal, Row} from 'react-bootstrap'
import '../Styles/ResultsTable.css'
import {mediaUrl} from '../Config'
import capitalize from "../Utils/capitalize";

class ResultsTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: this.props.data,
            showModal: false,
            modalImagePath: null
        };
    }

    componentDidMount() {
        window.scrollTo(0, 0);
    }

    showModal = imagePath => event => {
        this.setState({showModal: true, modalImagePath: imagePath})
    };

    renderDetections = predictions => {
        return predictions.map((item, index) => {
            let class_ = capitalize(item['predictions'][0]['class']);
            let probability = item['predictions'][0]['probability'].toFixed(2);

            if (probability < 0.6) {
                class_ = 'Unknown';
                probability = 0
            }
            return (
                <Card className='resultsSmallCard' key={index}>
                    <Card.Img variant="top" src={`${mediaUrl}/${item.image_path}`}
                              className='cigaretteImage'
                              onClick={this.showModal(`${mediaUrl}/${item.image_path}`)}/>
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
                                                          defaultValue={class_}
                                            />
                                        </div>
                                    </Form>
                                </Col>
                            </Row>
                        </ListGroupItem>
                        <ListGroupItem className='resultsListItem'>
                            <Row>
                                <Col className='nameTarget'>
                                    Probability:
                                </Col>
                                <Col>
                                    {probability}
                                </Col>
                            </Row>
                        </ListGroupItem>

                    </ListGroup>
                </Card>
            )
        })
    };

    render() {

        return (
            <div>
                <Card className="resultsMainCard">
                    <Row>
                        <Card className='resultsSmallCard' style={{height: 'auto'}}>
                            <Card.Img variant="top" src={`${mediaUrl}/${this.state.data.image.image_path}`}
                                      className='cigaretteImage'
                                      onClick={this.showModal(`${mediaUrl}/${this.state.data.image.image_path}`)}/>
                            <ListGroup className="list-group-flush">
                                <ListGroupItem className='resultsListItem'>
                                    <Row>
                                        <Col className='nameTarget'>
                                            Found {this.state.data.image['found_objects']} packs of cigarette
                                        </Col>

                                    </Row></ListGroupItem>
                            </ListGroup>
                        </Card>

                        {this.renderDetections(this.state.data.detections)}
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
    const {image_path} = {...props};
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