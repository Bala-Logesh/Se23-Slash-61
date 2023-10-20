import { render, screen } from "@testing-library/react";
import TestHelper from "../utils/TestHelper";
import Login from "../components/Login";

test("renders login page", () => {
    render(
        <TestHelper>
            <Login />
        </TestHelper>
    );
    const element = screen.getAllByText(/Hello there!/i);
    expect(element[0]).toBeInTheDocument();
});