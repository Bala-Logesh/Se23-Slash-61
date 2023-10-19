import { render, screen } from "@testing-library/react";
import App from "./App"

test("renders slash", () => {
  render(<App />);
  const linkElement = screen.getAllByText(/Slash/i);
  expect(linkElement[0]).toBeInTheDocument();
});
