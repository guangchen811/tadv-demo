export function LogoSection() {
  return (
    <div className="flex items-center gap-3 absolute left-1/2 transform -translate-x-1/2">
      {/* Diamond Icon */}
      <svg
        width="28"
        height="28"
        viewBox="0 0 28 28"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="flex-shrink-0"
      >
        <defs>
          <linearGradient id="diamondGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#6db4f2" />
            <stop offset="50%" stopColor="#4a90e2" />
            <stop offset="100%" stopColor="#3a7bc8" />
          </linearGradient>
        </defs>

        {/* Top facet (lightest) */}
        <path
          d="M14 2 L24 14 L14 10 L4 14 Z"
          fill="#6db4f2"
        />

        {/* Left facet (medium) */}
        <path
          d="M14 10 L4 14 L14 26 Z"
          fill="#4a90e2"
        />

        {/* Right facet (darker) */}
        <path
          d="M14 10 L24 14 L14 26 Z"
          fill="#3a7bc8"
        />

        {/* Bottom facet (darkest) */}
        <path
          d="M14 26 L4 14 L14 22 L24 14 Z"
          fill="#2d5f9e"
          opacity="0.8"
        />
      </svg>

      {/* Text Logo */}
      <div className="flex items-baseline font-bold text-lg leading-none">
        <span className="text-text-primary">Ta</span>
        <span className="text-accent-blue">DV</span>
      </div>
    </div>
  );
}
