const ResultPlayerCard = ({ name, bet, balance, cards }) => {
    return (
        <>
            <div className="border">
                <div>Name: {name}</div>
                <div>Bet: {bet}</div>
                <div>Balance: {balance}</div>
                <div>Cards: {cards && cards.map(card => { return <img className="d-inline" src={"/images/" + card + ".jpg"} alt={card} width="120" height="180"></img>})}</div>
            </div>
        </>
    )
};

export default ResultPlayerCard;