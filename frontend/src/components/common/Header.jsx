import { useNavigate } from "react-router-dom";
import * as game from "../../game";

// TODO: 可看到自己的 points

const Header = ({ isLogin, setIsLogin }) => {
    const name = sessionStorage.getItem("name");
    const nav = useNavigate();

    return (
        <>
            <div className="d-flex justify-content-end align-items-center bg-light">
                {isLogin && <div className="me-1">Name: {name}</div>}
                {isLogin && <button type="button" className="btn btn-outline-secondary me-1" onClick={() => handleLogoutBtnClick(setIsLogin, nav)}>Logout</button>}
                {isLogin && <button type="button" className="btn btn-outline-secondary" onClick={() => {
                    game.getPoints((points) => {
                        alert("You have " + points + " points.");
                    })
                }}>Get points</button>}
            </div>
        </>
    )
};

const handleLogoutBtnClick = (setIsLogin, nav) => {
    sessionStorage.removeItem("isLogin");
    sessionStorage.removeItem("name");
    setIsLogin(false);
    // 通知 server 移除 session
    game.logout(() => {
        return nav("/");
    })
}

export default Header;