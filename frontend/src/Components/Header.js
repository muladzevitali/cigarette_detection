import React from 'react'
import {Navbar} from 'react-bootstrap'
import '../Styles/Header.css'

class Header extends React.Component {
    render() {
        let style = {
            marginTop: '12%',
            marginBottom: '2%',
            textAlign: 'center',
            display: 'inline-table'
        };
        let imageSizes = {width:'102px'};

        if (this.props.style) {
            style = this.props.style;
            imageSizes.width = '61px';
        }

        return (
            <Navbar variant='dark' style={style}>
                <Navbar.Brand href='/'>
                    <img
                        src={"/cigaretteLogoGreen.png"}
                        {...imageSizes}
                        className="d-inline-block align-top"
                        alt="cigaretteLogo"
                    />

                </Navbar.Brand>


            </Navbar>
        )
    }
}


export default Header