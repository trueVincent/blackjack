import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import * as game from "../game";

const HomePage = ({ isLogin, setIsLogin }) => {
    const navigate = useNavigate();
    const [name, setName] = useState("");

    return (
        <>
            <div className="d-flex justify-content-center">
                <div className="fs-1 fw-bold">BlackJack</div>
            </div>
            <div className="d-flex flex-column align-items-center">
                {!isLogin && <input type="text" className="" placeholder="Name" onInput={(e) => setName(e.target.value)}/>}
                <div className="mt-2">
                    {!isLogin && <button className="w-100 btn btn-outline-secondary" type="button" onClick={() => loginBtnClickEvent(name, setIsLogin)}>Login</button>}
                    {!isLogin && <button className="mt-1 w-100 btn btn-outline-secondary" type="button" onClick={() => registerBtnClickEvent(name)}>Register</button>}
                    {isLogin && <button className="mt-1 w-100 btn btn-outline-secondary" type="button" onClick={() => joinBtnClickEvent(navigate)}>Join</button>}
                </div>
            </div>
        </>
    );
};

const loginBtnClickEvent = (name, setIsLogin) => {
    game.login(name, () => {
        setIsLogin(true);
        sessionStorage.setItem("name", name);
        sessionStorage.setItem("isLogin", "true");
    });
}

const registerBtnClickEvent = (name) => {
    game.register(name, () => {
        alert("註冊成功，name：" + name);
    });
}

const joinBtnClickEvent = (nav) => {
    game.join(() => {
        return nav("/waitingroom");
    })
}

export default HomePage;