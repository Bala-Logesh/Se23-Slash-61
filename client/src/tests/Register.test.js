import { render, screen } from "@testing-library/react";
import TestHelper from "../utils/TestHelper";
import Register from "../components/Register";

test("renders register page", () => {
  render(
    <TestHelper>
      <Register />
    </TestHelper>
  );
  const element = screen.getAllByText(/Hello there!/i);
  expect(element[0]).toBeInTheDocument();
});