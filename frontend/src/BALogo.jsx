export const BALogo = ({ className }) => (
    <svg
        viewBox="0 0 500 60"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className={className}
        aria-label="British Airways Logo"
    >
        {/* Speedmarque Ribbon */}
        <path
            d="M10 25 C 40 10, 80 5, 110 15 C 80 20, 40 30, 10 25 Z"
            fill="#EB2226"
        />
        <path
            d="M10 30 C 40 20, 80 15, 105 20 C 75 28, 35 38, 10 30 Z"
            fill="#075AAA"
        />

        {/* Text: BRITISH AIRWAYS */}
        <text
            x="130"
            y="42"
            fontFamily="'Times New Roman', Times, serif"
            fontWeight="700"
            fontSize="38"
            fill="#00295A"
            letterSpacing="1"
        >
            BRITISH AIRWAYS
        </text>
    </svg>
);

export const Speedmarque = () => (
    <svg width="60" height="30" viewBox="0 0 60 30" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M0 25C15 10 40 0 60 5" stroke="#EB2226" strokeWidth="4" strokeLinecap="round" />
        <path d="M5 28C18 15 40 8 55 12" stroke="#00295A" strokeWidth="2.5" strokeLinecap="round" />
    </svg>
);
