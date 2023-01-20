import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState } from 'react';

import HomePage from './pages/HomePage';
import WaitingRoomPage from './pages/WaitingRoomPage';
import GamePage from './pages/GamePage';
import ResultPage from './pages/ResultPage';
import Header from './components/common/Header';
import Footer from './components/common/Footer';

function App() {
  const [isLogin, setIsLogin] = useState(sessionStorage.getItem("isLogin") === "true" ? true : false);

  return (
    <div className="App">
      <BrowserRouter>
        <Header isLogin={isLogin} setIsLogin={setIsLogin}/>

        <div className="d-flex justify-content-center bg-secondary bg-gradient mb-2">
          <div className="fs-1 fw-bold fst-italic">BlackJack</div>
        </div>

        <Routes>
          <Route path="/" element={<HomePage isLogin={isLogin} setIsLogin={setIsLogin}/>} />
          {isLogin && <Route path="/waitingroom" element={<WaitingRoomPage />} />}
          {isLogin && <Route path="/game" element={<GamePage />} />}
          {isLogin && <Route path="/result" element={<ResultPage />} />}
        </Routes>
        
        <Footer />
      </BrowserRouter>
    </div>
  );
}

export default App;
