import React from 'react';
import axios from 'axios'
import SearchBar from './SearchBar'
import Header from './Header'
import ResultsTable from './ResultsTable'
import PageLoader from './PageLoader'
import {detectionUrl} from '../Config'
import {Container, Col, Row} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import '../Styles/App.css';


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: null,
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
        const params = {localize: data.localize, classify: data.classify, image: data.image};
        console.log(params, detectionUrl);
        axios.post(detectionUrl,
            {params})
            .then(
                (response) => {
                    this.setState({data: response.data.data || [], searchBarData: data, requestLoading: false})
                }
            ).catch(error => {
            data = {...data, errorMessage: 'Connection problem', validated: false};
            this.setState({requestLoading: false, searchBarData: data,});
            console.log(error)
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
                {this.state.data ?
                    (
                        <Container fluid className='dataContainer'>
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
                                <Col xs='10' style={{paddingLeft: '10%', marginTop: '1%'}}>
                                    <ResultsTable data={this.state.data}/>
                                </Col>
                            </Row>
                        </Container>
                    ) : (
                        <div>
                            <Header/>
                            <Container>
                                <SearchBar onSubmit={this.handleFormSubmit}
                                           state={this.state.searchBarData}/>
                            </Container>
                        </div>
                    )
                }
            </div>
        );
    }
}


export default App;
