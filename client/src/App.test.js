import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders slash", () => {
  render(<App />);
  const title = screen.getAllByText(/Slash/i);
  expect(title[0]).toBeInTheDocument();
});
