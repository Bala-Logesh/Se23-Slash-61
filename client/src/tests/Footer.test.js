import { render, screen } from "@testing-library/react";
import Footer from "../components/Footer";

test("renders footer", () => {
  render(<Footer />);
  const element = screen.getAllByText(/SE23 by Group 61/i);
  expect(element[0]).toBeInTheDocument();
});