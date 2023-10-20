import { render, screen } from "@testing-library/react";
import Card from "../components/Card";

test("renders card component", () => {
  render(<Card><p>Hello from CSC 510 - Group 61</p></Card>);
  const element = screen.getAllByText(/Hello from CSC 510 - Group 61/i);
  expect(element[0]).toBeInTheDocument();
});