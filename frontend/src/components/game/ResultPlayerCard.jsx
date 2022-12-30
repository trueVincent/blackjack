const ResultPlayerCard = ({ name, bet, balance, cards }) => {
    return (
        <>
            <div className="border">
                <div>Name: {name}</div>
                <div>Bet: {bet}</div>
                <div>Balance: {balance}</div>
                <div>Cards: {cards && cards.map(card => { return card + " " })} </div>
            </div>
        </>
    )
};

export default ResultPlayerCard;