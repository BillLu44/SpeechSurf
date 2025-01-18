import { Link } from "react-router-dom"
import "../App.css"


export default function Navbar() {
    return (
        <div className="navbar">
            <div className="nav-logo"><img src="/SpeechSurf.png"/></div>
            <Link to="/" className="nav-title">SpeechSurf</Link>
            <ul className="nav-btn-container">
                <li><Link to="/">HOME</Link></li>
                <li><Link to="/about">ABOUT</Link></li>
            </ul>
        </div>
    )
}