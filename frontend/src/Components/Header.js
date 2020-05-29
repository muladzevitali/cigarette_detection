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
        let imageSizes = {width:'360'};

        if (this.props.style) {
            style = this.props.style;
            imageSizes.width = '150px';
        }

        return (
            <Navbar variant='dark' style={style}>
                <Navbar.Brand href='/'>
                    <img
                        src={"/cigaretteDetectorLogo.png"}
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