import "../styles/cards.css";

function Card({ children, result = false }) {
  return <div className={result ? "card result" : "card"}>{children}</div>;
}

export default Card;