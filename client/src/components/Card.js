import "../styles/cards.css";
import "../styles/forms.css";

function Card({ children, result = false }) {
  return <div className={result ? "card result" : "card"}>{children}</div>;
}

export default Card;