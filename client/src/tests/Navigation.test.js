import { render, screen } from "@testing-library/react";
import TestHelper from "../utils/TestHelper";
import Navigation from "../components/Navigation";

test("renders navigation", () => {
  render(
    <TestHelper>
      <Navigation />
    </TestHelper>
  );
  const element = screen.getAllByText(/Slash/i);
  expect(element[0]).toBeInTheDocument();
});