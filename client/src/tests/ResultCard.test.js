import { render, screen } from "@testing-library/react";
import TestHelper from "../utils/TestHelper";
import products from "../data/products";
import ResultCard from "../components/ResultCard";

test("renders result card component", () => {
    const product = products[0];
    render(
        <TestHelper>
            <ResultCard product={product} />
        </TestHelper>
    );
    const element = screen.getAllByText(
        /2021 Newest Dell Inspiron 5515 Touch Lap/i
    );
    expect(element[0]).toBeInTheDocument();
});