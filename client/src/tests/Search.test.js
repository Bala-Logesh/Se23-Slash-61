import { render, screen } from "@testing-library/react";
import TestHelper from "../utils/TestHelper";
import Search from "../components/Search";

test("renders slash search page", () => {
    render(
        <TestHelper>
            <Search />
        </TestHelper>
    );
    const element = screen.getAllByText(/Search to your heart's content/i);
    expect(element[0]).toBeInTheDocument();
});