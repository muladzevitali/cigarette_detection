import React from 'react'
import {Button, Col, Form, Image, InputGroup} from 'react-bootstrap'
import '../Styles/SearchBar.css'


class SearchBar extends React.Component {
    constructor(props) {
        super(props);
        this.filterCommas = new RegExp(',', 'g');
        this.state = {
            showFilters: false,
            validated: null,
            errorMessage: null,
            imageName: null,
            ...props.state
        }
    }

    filterButtonHandler = () => {
        const showFilters = this.state.showFilters;
        this.setState({showFilters: !showFilters})
    };
    onChangeImage = (event) => {
        console.log(event.target.name, event.target, event.target.path)
        this.setState({[event.target.name]: event.target.value})
        this.setState({imageName: event.target.value})
    };

    onCheck = (event) => {
        this.setState({[event.target.name]: !this.state[event.target.name]})
    }
    isFormValid = data => {
        const {image} = {...data};
        if (!image) {
            this.setState({errorMessage: 'Please choose an image to continue processing'});
            return false
        }

    };
    onFormSubmit = event => {
        event.preventDefault();
        const data = {
            queryWord: event.target[1].value,
            minViews: event.target[3].value.replace(this.filterCommas, ''),
            maxViews: event.target[4].value.replace(this.filterCommas, '')
        };

        if (!this.isFormValid(data)) {
            event.stopPropagation();
            this.setState({validated: false});
            return
        }

        this.setState({validated: true});
        this.props.onSubmit(data)

    };

    render() {
        let searchButtonStyle = this.state.image.length > 2 ? {filter: 'invert(0.6) brightness(2.0)'} : {filter: 'invert(0.3)'};

        return (
            <Form noValidate onSubmit={this.onFormSubmit}>
                <Form.Row>
                    <Form.Group as={Col}>
                        <InputGroup size="lg" className={!this.state.image && 'is-invalid'}>
                            <InputGroup.Prepend>
                                <Button variant='none' className='searchButton' type='submit'>
                                    <Image src={'/searchButton.png'} alt="searchButton"
                                           style={searchButtonStyle}/>
                                </Button>
                            </InputGroup.Prepend>
                            <Form.File id="formcheck-api-custom"
                                       custom
                                       className='upload'

                                       required>
                                <Form.File.Input accept="image/*"
                                                 onChange={this.onChangeImage}
                                                 name='image'/>
                                <span className='fileName'>{this.state.imageName || 'Select file..'}</span>
                                <input type="button" className="uploadButton" value="Browse"/>

                            </Form.File>

                            <InputGroup.Append>
                                <Button variant='none' className='filterButton'
                                        size='sm'
                                        onClick={this.filterButtonHandler}
                                        onAnimationEnd={this.filterButtonHandler}>
                                    <Image alt="filterButton"
                                           src='filterButtonGreen.png'
                                           style={!this.state.showFilters ? {filter: 'invert(0.5)'} : {}}/>
                                </Button>
                            </InputGroup.Append>
                        </InputGroup>
                        <Form.Control.Feedback type='invalid'>
                            {this.state.errorMessage}
                        </Form.Control.Feedback>
                    </Form.Group>
                </Form.Row>

                <Form.Row className='searchFilterRow'
                          style={{
                              display: this.state.showFilters || 'none',
                              left: this.props.header ? '35%' : '45%'
                          }}>
                    <Form.Group as={Col} controlId="localize" md='6'>
                        <Form.Check
                            custom
                            inline
                            className='imageFilter'
                            label="Localize"
                            name='localize'
                            checked={this.state.localize === true}
                            onChange={this.onCheck}
                            id='custom-inline-checkbox-1'
                        />

                    </Form.Group>
                    <Form.Group as={Col} controlId="classify" md='6'>
                        <Form.Check
                            custom
                            inline
                            className='imageFilter'
                            label="Classify"
                            name='classify'
                            checked={this.state.classify === true}
                            onChange={this.onCheck}
                            id='custom-inline-checkbox-2'
                        />
                    </Form.Group>
                </Form.Row>

            </Form>
        )
    }

}

export default SearchBar