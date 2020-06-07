import React from 'react';
import axios from 'axios'
import SearchBar from './SearchBar'
import Header from './Header'
import ResultsTable from './ResultsTable'
import PageLoader from './PageLoader'
import {detectionUrl} from '../Config'
import {Col, Container, Row} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../Styles/App.css';


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: null,
            errorMessage: null,
            searchBarData: {
                classify: true,
                localize: true,
                image: ''
            },
            requestLoading: false,
        }
    }

    handleFormSubmit = (data) => {
        this.setState({requestLoading: true});
        // Create form
        let bodyFormData = new FormData();
        bodyFormData.append('image', data.image);
        bodyFormData.append('localize', data.localize);
        bodyFormData.append('classify', data.classify);
        // Send form and handle results
        axios.post(detectionUrl, bodyFormData)
            .then(
                (response) => {
                    this.setState({
                        data: response.data.data || [],
                        searchBarData: data,
                        requestLoading: false,
                        errorMessage: null
                    })
                }
            )
            .catch(error => {
                let errorMessage = 'Connection error';
                console.log('error', error.response);
                if (error.response && error.response.data && typeof error.response.data.message === 'string') {
                    errorMessage = error.response.data.message;
                }
                data = {errorMessage: errorMessage, validated: false};
                this.setState({requestLoading: false, errorMessage: errorMessage});
            });


    };

    render() {
        const dataHeaderStyle = {
            paddingLeft: null,
            paddingTop: '2%',
            marginLeft: '30%'
        };
        const dataSearchBarStyle = {
            paddingTop: '0.6rem'
        };
        if (this.state.requestLoading) {
            return <PageLoader/>
        }

        return (
            <div className='App align-self-center'>
                {!this.state.errorMessage && this.state.data ?
                    (
                        <Container fluid className='dataContainer align-self-center'>
                            <Row style={{alignContent: 'baseline'}}>
                                <Col xs='3' md='2'>
                                    <Header style={dataHeaderStyle}/>
                                </Col>
                                <Col xs='8' md='6' style={dataSearchBarStyle}>
                                    <SearchBar onSubmit={this.handleFormSubmit}
                                               state={this.state.searchBarData}
                                               header={true}/>
                                </Col>

                            </Row>
                            <Row>

                                <Col xs='10' style={{paddingLeft: '10%', marginTop: '1%'}}
                                     className='align-self-center'>
                                    <ResultsTable data={this.state.data}/>
                                </Col>
                            </Row>
                        </Container>
                    ) : (
                        <div>
                            <Header/>
                            <Container>
                                <SearchBar onSubmit={this.handleFormSubmit}
                                           state={this.state.searchBarData}
                                           errorMessage={this.state.errorMessage}/>
                            </Container>
                        </div>
                    )
                }
            </div>
        );
    }
}


export default App;
