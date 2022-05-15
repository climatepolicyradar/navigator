interface IconProps {
  width?: string;
  height?: string;
  color?: string;
}
export function CloseIcon({
  width = '20',
  height = '20',
  color = 'currentColor',
}: IconProps) {
  return (
    <svg
      style={{ width: `${width}px`, height: `${height}px` }}
      version="1.1"
      id="Capa_1"
      fill={color}
      xmlns="http://www.w3.org/2000/svg"
      x="0px"
      y="0px"
      viewBox="0 0 341.751 341.751"
    >
      <g>
        <g>
          <rect
            x="-49.415"
            y="149.542"
            transform="matrix(0.7072 -0.707 0.707 0.7072 -70.7868 170.8326)"
            width="440.528"
            height="42.667"
          />
        </g>
      </g>
      <g>
        <g>
          <rect
            x="149.569"
            y="-49.388"
            transform="matrix(0.707 -0.7072 0.7072 0.707 -70.7712 170.919)"
            width="42.667"
            height="440.528"
          />
        </g>
      </g>
    </svg>
  );
}

export function DocumentsIcon({
  width,
  height,
  color = 'currentColor',
}: IconProps) {
  return (
    <svg
      version="1.1"
      fill={color}
      id="Capa_1"
      xmlns="http://www.w3.org/2000/svg"
      style={{ width: `${width}px`, height: `${height}px` }}
      x="0px"
      y="0px"
      viewBox="0 0 957.599 957.6"
    >
      <g>
        <path
          d="M817.9,108.4h-28v687.901c0,45.699-37.2,82.898-82.899,82.898H423.3H197.7v25.5c0,29.201,23.7,52.9,52.9,52.9h283.6H817.8
        c29.2,0,52.899-23.699,52.899-52.9V161.3C870.7,132.1,847.1,108.4,817.9,108.4z"
        />
        <path
          d="M423.3,849.199h283.6c29.2,0,52.9-23.699,52.9-52.898V108.4V52.9c0-29.2-23.7-52.9-52.9-52.9H423.3H329v17.5
        c0.199,1.8,0.3,3.7,0.3,5.6v115.3V168c0,41.1-33.4,74.5-74.5,74.5h-29.6H109.9c-1.5,0-3.1-0.1-4.6-0.2H86.9v554.001
        c0,29.199,23.7,52.898,52.9,52.898h58H423.3L423.3,849.199z M434,669.4H249.1c-13.8,0-25-11.201-25-25c0-13.801,11.2-25,25-25h185
        c13.8,0,25,11.199,25,25C459.1,658.199,447.8,669.4,434,669.4z M619,541.801H249.1c-13.8,0-25-11.201-25-25c0-13.801,11.2-25,25-25
        H619c13.8,0,25,11.199,25,25C644,530.6,632.8,541.801,619,541.801z M249.1,356.3H619c13.8,0,25,11.2,25,25c0,13.8-11.2,25-25,25
        H249.1c-13.8,0-25-11.2-25-25C224.1,367.5,235.3,356.3,249.1,356.3z"
        />
        <path
          d="M109.9,212.5h144.9c0.1,0,0.3,0,0.4,0c24.2-0.2,43.8-19.8,44-44c0-0.1,0-0.3,0-0.4v-145c0-13.4-11-22.3-22.399-22.3
        c-5.5,0-11,2-15.6,6.6L94.1,174.5C80.1,188.5,90,212.5,109.9,212.5z"
        />
      </g>
    </svg>
  );
}

export function JurisdictionsIcon({
  width,
  height,
  color = 'currentColor',
}: IconProps) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill={color}
      style={{ width: `${width}px`, height: `${height}px` }}
      version="1.1"
      viewBox="0 0 512 512.0001"
    >
      <g id="surface1">
        <path d="M 15 512 L 287 512 C 295.285156 512 302 505.285156 302 497 L 302 481 C 302 464.429688 288.570312 451 272 451 L 272 433.066406 C 272 409.320312 252.679688 390 228.933594 390 L 73.066406 390 C 49.320312 390 30 409.320312 30 433.066406 L 30 451 C 13.429688 451 0 464.429688 0 481 L 0 497 C 0 505.28125 6.71875 512 15 512 Z M 15 512 " />
        <path d="M 187.734375 330.34375 C 197.703125 343.574219 216.515625 346.21875 229.746094 336.246094 C 242.980469 326.277344 245.621094 307.464844 235.652344 294.230469 L 145.378906 174.4375 C 135.40625 161.203125 116.597656 158.5625 103.367188 168.53125 C 90.132812 178.503906 87.488281 197.3125 97.460938 210.546875 Z M 187.734375 330.34375 " />
        <path d="M 403.363281 167.851562 C 413.335938 181.082031 432.144531 183.726562 445.378906 173.753906 C 458.609375 163.785156 461.253906 144.976562 451.28125 131.742188 L 361.007812 11.949219 C 351.039062 -1.285156 332.226562 -3.929688 318.996094 6.042969 C 305.765625 16.015625 303.121094 34.824219 313.09375 48.058594 Z M 403.363281 167.851562 " />
        <path d="M 337.5625 255 C 359.734375 238.292969 376.378906 217.546875 386.789062 195.703125 L 281.75 56.3125 C 257.882812 60.300781 233.355469 70.578125 211.179688 87.289062 C 189.007812 103.996094 172.363281 124.742188 161.953125 146.582031 L 266.992188 285.980469 C 290.859375 281.992188 315.386719 271.710938 337.5625 255 Z M 337.5625 255 " />
        <path d="M 378.066406 258.90625 C 371.082031 266.023438 363.726562 272.847656 355.617188 278.960938 C 347.503906 285.070312 338.914062 290.261719 330.152344 295.015625 L 349.710938 320.972656 L 397.628906 284.867188 Z M 378.066406 258.90625 " />
        <path d="M 415.683594 308.824219 L 367.765625 344.929688 L 458.039062 464.726562 C 468.011719 477.960938 486.820312 480.601562 500.050781 470.632812 C 513.285156 460.660156 515.925781 441.851562 505.957031 428.617188 Z M 415.683594 308.824219 " />
      </g>
    </svg>
  );
}

export function AddIcon({ width, height, color = 'currentColor' }: IconProps) {
  return (
    <svg
      id="bold"
      style={{ width: `${width}px`, height: `${height}px` }}
      fill={color}
      enableBackground="new 0 0 24 24"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path d="m14.25 0h-11.5c-1.52 0-2.75 1.23-2.75 2.75v15.5c0 1.52 1.23 2.75 2.75 2.75h6.59c-.54-1.14-.84-2.41-.84-3.75 0-1.15.22-2.25.63-3.26-.04.01-.08.01-.13.01h-5c-.55 0-1-.45-1-1s.45-1 1-1h5c.38 0 .72.22.88.54.65-1.01 1.49-1.87 2.48-2.54h-8.36c-.55 0-1-.45-1-1s.45-1 1-1h9c.55 0 1 .45 1 1 0 .05 0 .09-.01.13.93-.38 1.95-.6 3.01-.62v-5.76c0-1.52-1.23-2.75-2.75-2.75zm-6.25 6h-4c-.55 0-1-.45-1-1s.45-1 1-1h4c.55 0 1 .45 1 1s-.45 1-1 1z" />
      <path d="m17.25 10.5c-3.722 0-6.75 3.028-6.75 6.75s3.028 6.75 6.75 6.75 6.75-3.028 6.75-6.75-3.028-6.75-6.75-6.75zm2.75 7.75h-1.75v1.75c0 .552-.448 1-1 1s-1-.448-1-1v-1.75h-1.75c-.552 0-1-.448-1-1s.448-1 1-1h1.75v-1.75c0-.552.448-1 1-1s1 .448 1 1v1.75h1.75c.552 0 1 .448 1 1s-.448 1-1 1z" />
    </svg>
  );
}

export function SearchIcon({
  width,
  height,
  color = 'currentColor',
}: IconProps) {
  return (
    <svg
      id="Layer_1"
      fill={color}
      style={{ width: `${width}px`, height: `${height}px` }}
      enableBackground="new 0 0 512.392 512.392"
      viewBox="0 0 512.392 512.392"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g>
        <path d="m211.196 422c-116.346 0-211-94.654-211-211s94.654-211 211-211 211 94.654 211 211-94.654 211-211 211zm0-382c-94.29 0-171 76.71-171 171s76.71 171 171 171 171-76.71 171-171-76.71-171-171-171zm295.143 466.534c7.81-7.811 7.81-20.475 0-28.285l-89.5-89.5c-7.811-7.811-20.475-7.811-28.285 0s-7.81 20.475 0 28.285l89.5 89.5c3.905 3.905 9.024 5.857 14.143 5.857s10.236-1.952 14.142-5.857z" />
      </g>
    </svg>
  );
}

export function MenuIcon({ color = 'currentColor' }: IconProps) {
  return (
    <svg
      viewBox="0 0 35 35"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      height="35"
      width="35"
    >
      <path
        d="M4.375 17.5H30.625M4.375 8.75H30.625M4.375 26.25H30.625"
        stroke="white"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function EditIcon({ color = 'currentColor' }) {
  return (
    <svg
      version="1.1"
      id="icon"
      xmlns="http://www.w3.org/2000/svg"
      x="0px"
      y="0px"
      width="32px"
      height="32px"
      viewBox="0 0 32 32"
      fill={color}
    >
      <rect x="2" y="26" width="28" height="2" />
      <path
        d="M25.4,9c0.8-0.8,0.8-2,0-2.8c0,0,0,0,0,0l-3.6-3.6c-0.8-0.8-2-0.8-2.8,0c0,0,0,0,0,0l-15,15V24h6.4L25.4,9z M20.4,4L24,7.6
      l-3,3L17.4,7L20.4,4z M6,22v-3.6l10-10l3.6,3.6l-10,10H6z"
      />
      <rect
        id="_Transparent_Rectangle_"
        width="32"
        height="32"
        style={{ fill: 'none' }}
      />
    </svg>
  );
}

export function DownloadIcon({
  height = '19',
  width = '23',
  color = 'currentColor',
}: IconProps) {
  return (
    <svg
      style={{ width: `${width}px`, height: `${height}px` }}
      viewBox="0 0 23 19"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M20.125 11.875V15.0417C20.125 15.4616 19.9231 15.8643 19.5636 16.1613C19.2042 16.4582 18.7167 16.625 18.2083 16.625H4.79167C4.28334 16.625 3.79582 16.4582 3.43638 16.1613C3.07693 15.8643 2.875 15.4616 2.875 15.0417V11.875M6.70833 7.91667L11.5 11.875M11.5 11.875L16.2917 7.91667M11.5 11.875V2.375"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function DownloadPDFIcon({
  height = '32',
  width = '32',
  color = 'currentColor',
}: IconProps) {
  return (
    <svg
      id="icon"
      xmlns="http://www.w3.org/2000/svg"
      style={{ width: `${width}px`, height: `${height}px` }}
      viewBox="0 0 32 32"
      fill={color}
    >
      <path d="M24,24v4H8V24H6v4H6a2,2,0,0,0,2,2H24a2,2,0,0,0,2-2h0V24Z" />
      <polygon points="21 21 19.586 19.586 17 22.172 17 14 15 14 15 22.172 12.414 19.586 11 21 16 26 21 21" />
      <polygon points="28 4 28 2 22 2 22 12 24 12 24 8 27 8 27 6 24 6 24 4 28 4" />
      <path d="M17,12H13V2h4a3.0033,3.0033,0,0,1,3,3V9A3.0033,3.0033,0,0,1,17,12Zm-2-2h2a1.0011,1.0011,0,0,0,1-1V5a1.0011,1.0011,0,0,0-1-1H15Z" />
      <path d="M9,2H4V12H6V9H9a2.0027,2.0027,0,0,0,2-2V4A2.0023,2.0023,0,0,0,9,2ZM6,7V4H9l.001,3Z" />
      <rect
        id="_Transparent_Rectangle_"
        data-name="&lt;Transparent Rectangle&gt;"
        style={{ fill: 'none' }}
        width="32"
        height="32"
      />
    </svg>
  );
}

export function ViewDocumentCoverPageIcon({
  height = '32',
  width = '32',
  color = 'currentColor',
}: IconProps) {
  return (
    <svg
      id="icon"
      xmlns="http://www.w3.org/2000/svg"
      style={{ width: `${width}px`, height: `${height}px` }}
      viewBox="0 0 32 32"
      fill={color}
    >
      <circle cx="22" cy="24" r="2" />
      <path
        id="_inner_path_"
        data-name="&lt;inner path&gt;"
        style={{ fill: 'none' }}
        d="M22,28a4,4,0,1,1,4-4A4.0039,4.0039,0,0,1,22,28Zm0-6a2,2,0,1,0,2,2A2.0027,2.0027,0,0,0,22,22Z"
      />
      <path d="M29.7769,23.4785A8.64,8.64,0,0,0,22,18a8.64,8.64,0,0,0-7.7769,5.4785L14,24l.2231.5215A8.64,8.64,0,0,0,22,30a8.64,8.64,0,0,0,7.7769-5.4785L30,24ZM22,28a4,4,0,1,1,4-4A4.0045,4.0045,0,0,1,22,28Z" />
      <path d="M12,28H8V4h8v6a2.0058,2.0058,0,0,0,2,2h6v4h2V10a.9092.9092,0,0,0-.3-.7l-7-7A.9087.9087,0,0,0,18,2H8A2.0058,2.0058,0,0,0,6,4V28a2.0058,2.0058,0,0,0,2,2h4ZM18,4.4,23.6,10H18Z" />
      <rect
        id="_Transparent_Rectangle_"
        data-name="&lt;Transparent Rectangle&gt;"
        style={{ fill: 'none' }}
        width="32"
        height="32"
      />
    </svg>
  );
}

export function DownArrowIcon({
  height = '16',
  width = '16',
  color = 'currentColor',
}: IconProps) {
  return (
    <svg
      style={{ width: `${width}px`, height: `${height}px` }}
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g fill={color} id="Layer_3" data-name="Layer 3">
        <path d="m18.646 6.354-6.646 6.646-6.646-6.646a1.914 1.914 0 0 0 -2.708 2.707l9 9a.5.5 0 0 0 .708 0l9-9a1.914 1.914 0 1 0 -2.708-2.707z" />
      </g>
    </svg>
  );
}

export function KebabMenuIcon({
  height = '23',
  width = '5',
  color = 'currentColor',
}: IconProps) {
  return (
    <svg
      style={{ width: `${width}px`, height: `${height}px` }}
      viewBox="0 0 5 23"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M2.5 4.9375C3.70812 4.9375 4.6875 3.95812 4.6875 2.75C4.6875 1.54188 3.70812 0.5625 2.5 0.5625C1.29188 0.5625 0.3125 1.54188 0.3125 2.75C0.3125 3.95812 1.29188 4.9375 2.5 4.9375ZM2.5 13.6875C3.70812 13.6875 4.6875 12.7081 4.6875 11.5C4.6875 10.2919 3.70812 9.3125 2.5 9.3125C1.29188 9.3125 0.3125 10.2919 0.3125 11.5C0.3125 12.7081 1.29188 13.6875 2.5 13.6875ZM4.6875 20.25C4.6875 21.4581 3.70812 22.4375 2.5 22.4375C1.29188 22.4375 0.3125 21.4581 0.3125 20.25C0.3125 19.0419 1.29188 18.0625 2.5 18.0625C3.70812 18.0625 4.6875 19.0419 4.6875 20.25Z"
        fill={color}
      />
    </svg>
  );
}

export function DownLongArrowIcon({
  height = '72',
  width = '12',
  color = 'currentColor',
}: IconProps) {
  return (
    <svg
      style={{ width: `${width}px`, height: `${height}px` }}
      viewBox="0 0 12 72"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M6 72L11.7735 62H0.226497L6 72ZM5 0L5 63H7L7 0L5 0Z"
        fill={color}
      />
    </svg>
  );
}
export function EyeIcon({
  height = '80',
  width = '80',
  color = 'currentColor',
}: IconProps) {
  return (
    <svg
      style={{ width: `${width}px`, height: `${height}px` }}
      viewBox="0 0 80 80"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M3.33325 39.9999C3.33325 39.9999 16.6666 13.3333 39.9999 13.3333C63.3332 13.3333 76.6666 39.9999 76.6666 39.9999C76.6666 39.9999 63.3332 66.6666 39.9999 66.6666C16.6666 66.6666 3.33325 39.9999 3.33325 39.9999Z"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M39.9999 49.9999C45.5228 49.9999 49.9999 45.5228 49.9999 39.9999C49.9999 34.4771 45.5228 29.9999 39.9999 29.9999C34.4771 29.9999 29.9999 34.4771 29.9999 39.9999C29.9999 45.5228 34.4771 49.9999 39.9999 49.9999Z"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
export function ReadMoreIcon({
  height = '60',
  width = '60',
  color = 'currentColor',
}: IconProps) {
  return (
    <svg
      id="Capa_1"
      fill={color}
      enableBackground="new 0 0 512 512"
      style={{ width: `${width}px`, height: `${height}px` }}
      viewBox="0 0 512 512"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g>
        <path d="m195 136h302c8.291 0 15-6.709 15-15s-6.709-15-15-15h-302c-8.291 0-15 6.709-15 15s6.709 15 15 15z" />
        <path d="m497 196h-242c-8.291 0-15 6.709-15 15s6.709 15 15 15h242c8.291 0 15-6.709 15-15s-6.709-15-15-15z" />
        <path d="m497 286h-242c-8.291 0-15 6.709-15 15s6.709 15 15 15h242c8.291 0 15-6.709 15-15s-6.709-15-15-15z" />
        <path d="m497 376h-302c-8.291 0-15 6.709-15 15s6.709 15 15 15h302c8.291 0 15-6.709 15-15s-6.709-15-15-15z" />
        <path d="m205.587 245.376-59.982-59.982c-5.859-5.859-15.352-5.859-21.211 0s-5.859 15.352 0 21.211l34.395 34.395h-143.789c-8.291 0-15 6.709-15 15s6.709 15 15 15h143.789l-34.395 34.395c-5.859 5.859-5.859 15.352 0 21.211s15.351 5.86 21.211 0l59.982-59.982c5.806-5.791 5.897-15.367 0-21.248z" />
      </g>
    </svg>
  );
}
