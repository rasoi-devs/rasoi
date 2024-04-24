function _randomNumber(min, max) {
  return Math.random() * (max - min) + min;
}

export default function Loading() {
  return (
    <div role="status" className="flex animate-pulse flex-col">
      <div className="h-10 w-[60rem] self-start rounded-full bg-background-200"></div>
      <div className="mt-3 flex h-64 w-full items-center justify-center self-center rounded-xl bg-background-300 sm:w-96">
        <svg
          className="h-10 w-10 text-background-200"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          fill="currentColor"
          viewBox="0 0 20 18"
        >
          <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z" />
        </svg>
      </div>
      <div className="mt-3 self-start">
        <div className="mb-4 h-8 w-[20rem] rounded-full bg-background-200" />
        {[...Array(50).keys()].map((i) => (
          <div
            key={i}
            style={{ width: `${_randomNumber(30, 80)}rem` }}
            className="mt-2 h-4 rounded-full bg-background-200"
          />
        ))}
      </div>
      <span className="sr-only">Loading...</span>
    </div>
  );
}
