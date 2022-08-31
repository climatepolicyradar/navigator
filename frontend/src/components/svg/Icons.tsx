interface IconProps {
  width?: string;
  height?: string;
  color?: string;
}
export function CloseIcon({ width = "20", height = "20", color = "currentColor" }: IconProps) {
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
          <rect x="-49.415" y="149.542" transform="matrix(0.7072 -0.707 0.707 0.7072 -70.7868 170.8326)" width="440.528" height="42.667" />
        </g>
      </g>
      <g>
        <g>
          <rect x="149.569" y="-49.388" transform="matrix(0.707 -0.7072 0.7072 0.707 -70.7712 170.919)" width="42.667" height="440.528" />
        </g>
      </g>
    </svg>
  );
}

export function DocumentsIcon({ width, height, color = "currentColor" }: IconProps) {
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

export function JurisdictionsIcon({ width, height, color = "currentColor" }: IconProps) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" fill={color} style={{ width: `${width}px`, height: `${height}px` }} version="1.1" viewBox="0 0 512 512.0001">
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

export function AddIcon({ width, height, color = "currentColor" }: IconProps) {
  return (
    <svg id="bold" style={{ width: `${width}px`, height: `${height}px` }} fill={color} enableBackground="new 0 0 24 24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="m14.25 0h-11.5c-1.52 0-2.75 1.23-2.75 2.75v15.5c0 1.52 1.23 2.75 2.75 2.75h6.59c-.54-1.14-.84-2.41-.84-3.75 0-1.15.22-2.25.63-3.26-.04.01-.08.01-.13.01h-5c-.55 0-1-.45-1-1s.45-1 1-1h5c.38 0 .72.22.88.54.65-1.01 1.49-1.87 2.48-2.54h-8.36c-.55 0-1-.45-1-1s.45-1 1-1h9c.55 0 1 .45 1 1 0 .05 0 .09-.01.13.93-.38 1.95-.6 3.01-.62v-5.76c0-1.52-1.23-2.75-2.75-2.75zm-6.25 6h-4c-.55 0-1-.45-1-1s.45-1 1-1h4c.55 0 1 .45 1 1s-.45 1-1 1z" />
      <path d="m17.25 10.5c-3.722 0-6.75 3.028-6.75 6.75s3.028 6.75 6.75 6.75 6.75-3.028 6.75-6.75-3.028-6.75-6.75-6.75zm2.75 7.75h-1.75v1.75c0 .552-.448 1-1 1s-1-.448-1-1v-1.75h-1.75c-.552 0-1-.448-1-1s.448-1 1-1h1.75v-1.75c0-.552.448-1 1-1s1 .448 1 1v1.75h1.75c.552 0 1 .448 1 1s-.448 1-1 1z" />
    </svg>
  );
}

export function SearchIcon({ width, height, color = "currentColor" }: IconProps) {
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

export function MenuIcon({ color = "currentColor" }: IconProps) {
  return (
    <svg viewBox="0 0 35 35" fill="none" xmlns="http://www.w3.org/2000/svg" height="35" width="35">
      <path d="M4.375 17.5H30.625M4.375 8.75H30.625M4.375 26.25H30.625" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function EditIcon({ color = "currentColor" }) {
  return (
    <svg version="1.1" id="icon" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="32px" height="32px" viewBox="0 0 32 32" fill={color}>
      <rect x="2" y="26" width="28" height="2" />
      <path
        d="M25.4,9c0.8-0.8,0.8-2,0-2.8c0,0,0,0,0,0l-3.6-3.6c-0.8-0.8-2-0.8-2.8,0c0,0,0,0,0,0l-15,15V24h6.4L25.4,9z M20.4,4L24,7.6
      l-3,3L17.4,7L20.4,4z M6,22v-3.6l10-10l3.6,3.6l-10,10H6z"
      />
      <rect id="_Transparent_Rectangle_" width="32" height="32" style={{ fill: "none" }} />
    </svg>
  );
}

export function DownloadIcon({ height = "19", width = "23", color = "currentColor" }: IconProps) {
  return (
    <svg style={{ width: `${width}px`, height: `${height}px` }} viewBox="0 0 23 19" fill="none" xmlns="http://www.w3.org/2000/svg">
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

export function DownloadPDFIcon({ height = "32", width = "32", color = "currentColor" }: IconProps) {
  return (
    <svg id="icon" xmlns="http://www.w3.org/2000/svg" style={{ width: `${width}px`, height: `${height}px` }} viewBox="0 0 32 32" fill={color}>
      <path d="M24,24v4H8V24H6v4H6a2,2,0,0,0,2,2H24a2,2,0,0,0,2-2h0V24Z" />
      <polygon points="21 21 19.586 19.586 17 22.172 17 14 15 14 15 22.172 12.414 19.586 11 21 16 26 21 21" />
      <polygon points="28 4 28 2 22 2 22 12 24 12 24 8 27 8 27 6 24 6 24 4 28 4" />
      <path d="M17,12H13V2h4a3.0033,3.0033,0,0,1,3,3V9A3.0033,3.0033,0,0,1,17,12Zm-2-2h2a1.0011,1.0011,0,0,0,1-1V5a1.0011,1.0011,0,0,0-1-1H15Z" />
      <path d="M9,2H4V12H6V9H9a2.0027,2.0027,0,0,0,2-2V4A2.0023,2.0023,0,0,0,9,2ZM6,7V4H9l.001,3Z" />
      <rect id="_Transparent_Rectangle_" data-name="&lt;Transparent Rectangle&gt;" style={{ fill: "none" }} width="32" height="32" />
    </svg>
  );
}

export function ViewDocumentCoverPageIcon({ height = "32", width = "32", color = "currentColor" }: IconProps) {
  return (
    <svg id="icon" xmlns="http://www.w3.org/2000/svg" style={{ width: `${width}px`, height: `${height}px` }} viewBox="0 0 32 32" fill={color}>
      <circle cx="22" cy="24" r="2" />
      <path
        id="_inner_path_"
        data-name="&lt;inner path&gt;"
        style={{ fill: "none" }}
        d="M22,28a4,4,0,1,1,4-4A4.0039,4.0039,0,0,1,22,28Zm0-6a2,2,0,1,0,2,2A2.0027,2.0027,0,0,0,22,22Z"
      />
      <path d="M29.7769,23.4785A8.64,8.64,0,0,0,22,18a8.64,8.64,0,0,0-7.7769,5.4785L14,24l.2231.5215A8.64,8.64,0,0,0,22,30a8.64,8.64,0,0,0,7.7769-5.4785L30,24ZM22,28a4,4,0,1,1,4-4A4.0045,4.0045,0,0,1,22,28Z" />
      <path d="M12,28H8V4h8v6a2.0058,2.0058,0,0,0,2,2h6v4h2V10a.9092.9092,0,0,0-.3-.7l-7-7A.9087.9087,0,0,0,18,2H8A2.0058,2.0058,0,0,0,6,4V28a2.0058,2.0058,0,0,0,2,2h4ZM18,4.4,23.6,10H18Z" />
      <rect id="_Transparent_Rectangle_" data-name="&lt;Transparent Rectangle&gt;" style={{ fill: "none" }} width="32" height="32" />
    </svg>
  );
}

export function DownArrowIcon({ height = "16", width = "16", color = "currentColor" }: IconProps) {
  return (
    <svg style={{ width: `${width}px`, height: `${height}px` }} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <g fill={color} id="Layer_3" data-name="Layer 3">
        <path d="m18.646 6.354-6.646 6.646-6.646-6.646a1.914 1.914 0 0 0 -2.708 2.707l9 9a.5.5 0 0 0 .708 0l9-9a1.914 1.914 0 1 0 -2.708-2.707z" />
      </g>
    </svg>
  );
}

export function KebabMenuIcon({ height = "23", width = "5", color = "currentColor" }: IconProps) {
  return (
    <svg style={{ width: `${width}px`, height: `${height}px` }} viewBox="0 0 5 23" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M2.5 4.9375C3.70812 4.9375 4.6875 3.95812 4.6875 2.75C4.6875 1.54188 3.70812 0.5625 2.5 0.5625C1.29188 0.5625 0.3125 1.54188 0.3125 2.75C0.3125 3.95812 1.29188 4.9375 2.5 4.9375ZM2.5 13.6875C3.70812 13.6875 4.6875 12.7081 4.6875 11.5C4.6875 10.2919 3.70812 9.3125 2.5 9.3125C1.29188 9.3125 0.3125 10.2919 0.3125 11.5C0.3125 12.7081 1.29188 13.6875 2.5 13.6875ZM4.6875 20.25C4.6875 21.4581 3.70812 22.4375 2.5 22.4375C1.29188 22.4375 0.3125 21.4581 0.3125 20.25C0.3125 19.0419 1.29188 18.0625 2.5 18.0625C3.70812 18.0625 4.6875 19.0419 4.6875 20.25Z"
        fill={color}
      />
    </svg>
  );
}

export function DownLongArrowIcon({ height = "72", width = "12", color = "currentColor" }: IconProps) {
  return (
    <svg style={{ width: `${width}px`, height: `${height}px` }} viewBox="0 0 12 72" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M6 72L11.7735 62H0.226497L6 72ZM5 0L5 63H7L7 0L5 0Z" fill={color} />
    </svg>
  );
}

export function RightArrowIcon({ height = "32", width = "32", color = "currentColor" }: IconProps) {
  return (
    <svg style={{ width: `${width}px`, height: `${height}px` }} viewBox="0 0 29 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M2 10.5C1.17157 10.5 0.5 11.1716 0.5 12C0.5 12.8284 1.17157 13.5 2 13.5V10.5ZM28.0607 13.0607C28.6464 12.4749 28.6464 11.5251 28.0607 10.9393L18.5147 1.3934C17.9289 0.807611 16.9792 0.807611 16.3934 1.3934C15.8076 1.97919 15.8076 2.92893 16.3934 3.51472L24.8787 12L16.3934 20.4853C15.8076 21.0711 15.8076 22.0208 16.3934 22.6066C16.9792 23.1924 17.9289 23.1924 18.5147 22.6066L28.0607 13.0607ZM2 13.5H27V10.5H2V13.5Z"
        fill={color}
      />
    </svg>
  );
}

export function EyeIcon({ height = "80", width = "80", color = "currentColor" }: IconProps) {
  return (
    <svg style={{ width: `${width}px`, height: `${height}px` }} viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
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
export function ReadMoreIcon({ height = "60", width = "60", color = "currentColor" }: IconProps) {
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

export function ExternalLinkIcon({ height = "32", width = "32", color = "currentColor" }: IconProps) {
  return (
    <svg id="icon" xmlns="http://www.w3.org/2000/svg" fill={color} style={{ width: `${width}px`, height: `${height}px` }} viewBox="0 0 32 32">
      <path d="M26,28H6a2.0027,2.0027,0,0,1-2-2V6A2.0027,2.0027,0,0,1,6,4H16V6H6V26H26V16h2V26A2.0027,2.0027,0,0,1,26,28Z" />
      <polygon points="20 2 20 4 26.586 4 18 12.586 19.414 14 28 5.414 28 12 30 12 30 2 20 2" />
      <rect id="_Transparent_Rectangle_" data-name="&lt;Transparent Rectangle&gt;" style={{ width: `${width}px`, height: `${height}px`, fill: "none" }} />
    </svg>
  );
}

export const LawIcon = ({ height = "32", width = "32", color = "currentColor" }: IconProps) => {
  return (
    <svg viewBox="0 0 40 43" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ width: `${width}px`, height: `${height}px` }}>
      <path
        d="M33.5938 0.00012207C37.0296 0.00012207 39.8148 3.00821 39.8148 6.71887C39.8148 10.4295 37.0296 13.4376 33.5938 13.4376C32.1931 13.4376 30.9006 12.9377 29.8608 12.0941L29.8611 33.5939C29.8611 38.7888 25.9617 43.0001 21.1516 43.0001H1.24421C-0.414738 43.0001 -0.414738 40.3126 1.24421 40.3126C4.24568 40.3126 5.80633 37.8805 5.80633 33.5939L5.80467 33.6996L5.80633 9.40637C5.80633 4.34132 9.51317 0.211303 14.1568 0.00796786L14.5158 0.00012207C14.6621 0.00012207 14.8025 0.0273816 14.9328 0.0774533C15.0598 0.0271501 15.1996 0.00012207 15.3453 0.00012207H33.5938ZM14.93 2.61093L14.8466 2.63962C14.7413 2.67091 14.6303 2.68762 14.5158 2.68762C11.08 2.68762 8.29475 5.69571 8.29475 9.40637L8.29309 33.5688L8.29475 33.5939C8.29475 33.6295 8.29465 33.6651 8.29446 33.7006L8.29475 34.4897C8.29475 34.6134 8.27928 34.7332 8.25031 34.8469L8.22435 35.1922C8.03694 37.2485 7.47673 38.9957 6.5599 40.3126H21.1516C24.5874 40.3126 27.3727 37.3045 27.3727 33.5939V6.71887L27.3813 6.36205C27.4479 4.98696 27.8974 3.72136 28.6167 2.68724L15.3453 2.68762C15.1996 2.68762 15.0598 2.66059 14.93 2.61093ZM23.64 29.5626C24.3272 29.5626 24.8843 30.1642 24.8843 30.9064C24.8843 31.6485 24.3272 32.2501 23.64 32.2501H12.0274C11.3402 32.2501 10.7832 31.6485 10.7832 30.9064C10.7832 30.1642 11.3402 29.5626 12.0274 29.5626H23.64ZM23.64 24.1876C24.3272 24.1876 24.8843 24.7892 24.8843 25.5314C24.8843 26.2735 24.3272 26.8751 23.64 26.8751H12.0274C11.3402 26.8751 10.7832 26.2735 10.7832 25.5314C10.7832 24.7892 11.3402 24.1876 12.0274 24.1876H23.64ZM23.64 18.8126C24.3272 18.8126 24.8843 19.4142 24.8843 20.1564C24.8843 20.8985 24.3272 21.5001 23.64 21.5001H12.0274C11.3402 21.5001 10.7832 20.8985 10.7832 20.1564C10.7832 19.4142 11.3402 18.8126 12.0274 18.8126H23.64ZM23.64 13.4376C24.3272 13.4376 24.8843 14.0392 24.8843 14.7814C24.8843 15.5235 24.3272 16.1251 23.64 16.1251H12.0274C11.3402 16.1251 10.7832 15.5235 10.7832 14.7814C10.7832 14.0392 11.3402 13.4376 12.0274 13.4376H23.64ZM33.5938 2.68762C31.5323 2.68762 29.8611 4.49247 29.8611 6.71887C29.8611 8.94527 31.5323 10.7501 33.5938 10.7501C35.6552 10.7501 37.3264 8.94527 37.3264 6.71887C37.3264 4.49247 35.6552 2.68762 33.5938 2.68762Z"
        fill={color}
      />
    </svg>
  );
};

export const PolicyIcon = ({ height = "32", width = "32", color = "currentColor" }: IconProps) => {
  return (
    <svg viewBox="0 0 44 42" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ width: `${width}px`, height: `${height}px` }}>
      <path
        d="M41.583 39.2627C42.3749 39.2627 43.0169 39.8755 43.0169 40.6314C43.0169 41.3873 42.3749 42.0001 41.583 42.0001H1.4339C0.641977 42.0001 0 41.3873 0 40.6314C0 39.8755 0.641977 39.2627 1.4339 39.2627H41.583ZM22.7693 0.272696L39.3356 7.86218L39.37 7.87815C39.4112 7.89837 39.4512 7.92044 39.49 7.94424L39.3356 7.86218C39.4082 7.89546 39.477 7.93411 39.5415 7.9775C39.5758 8.00053 39.609 8.02506 39.641 8.0509C39.6601 8.06634 39.6783 8.08184 39.6961 8.09775C39.7234 8.12221 39.7515 8.14939 39.7783 8.17765C39.7965 8.1968 39.8141 8.21649 39.8311 8.23662C39.855 8.26486 39.8776 8.29381 39.899 8.32361C39.9124 8.34256 39.9254 8.36173 39.9379 8.38119C40.0718 8.58894 40.1491 8.83393 40.1491 9.09614V13.038C40.1491 14.5324 38.8523 15.7207 37.2813 15.7207V28.7509C38.8523 28.7509 40.1491 29.9392 40.1491 31.4336V34.0064L41.583 34.0068C42.3089 34.0068 42.9088 34.5217 43.0038 35.1898L43.0169 35.3755C43.0169 36.1315 42.3749 36.7442 41.583 36.7442H1.4339C0.641977 36.7442 0 36.1315 0 35.3755C0 34.6196 0.641977 34.0068 1.4339 34.0068L2.86779 34.0064V31.4336C2.86779 29.9392 4.16454 28.7509 5.73558 28.7509V15.7207C4.16454 15.7207 2.86779 14.5324 2.86779 13.038V9.09614L2.88088 8.91041C2.90818 8.71834 2.97722 8.53893 3.07899 8.38078C3.09145 8.36173 3.10445 8.34256 3.11794 8.32371C3.13924 8.29381 3.16182 8.26486 3.18554 8.23682C3.20277 8.21649 3.22039 8.1968 3.23861 8.17759C3.26538 8.14939 3.29341 8.12221 3.32257 8.09618C3.33853 8.08184 3.35675 8.06634 3.37541 8.05127C3.40788 8.02506 3.44107 8.00053 3.47537 7.9774C3.49238 7.96605 3.5097 7.95492 3.52731 7.94414C3.56565 7.92044 3.60569 7.89837 3.64689 7.87815C3.65863 7.87272 3.66989 7.86739 3.68125 7.86218L20.2499 0.271605C21.0442 -0.0905538 21.9727 -0.0905537 22.7693 0.272696ZM7.08918 31.4825H5.73558V34.0068H37.2813V31.4884H30.1118L30.0927 31.4861L24.4114 31.488C24.3997 31.4882 24.388 31.4884 24.3762 31.4884H18.6406L18.5909 31.4843L12.9694 31.487C12.9481 31.4879 12.9266 31.4884 12.9051 31.4884H7.16948L7.08918 31.4825ZM17.2067 15.7203H14.339V28.7505H17.2067V15.7203ZM28.6779 15.7203H25.8101V28.7505H28.6779V15.7203ZM11.4712 15.7207H8.60337V28.7509H11.4712V15.7207ZM22.9423 15.7207H20.0745V28.7509H22.9423V15.7207ZM34.4135 15.7207H31.5457V28.7509H34.4135V15.7207ZM37.2813 10.4644H5.73558V12.9833L37.2857 12.9844L37.2813 10.4644ZM21.4884 2.74061L10.6032 7.72699H32.4137L21.5309 2.7417C21.5183 2.736 21.4985 2.736 21.4884 2.74061Z"
        fill={color}
      />
    </svg>
  );
};

export const CaseIcon = ({ height = "32", width = "32", color = "currentColor" }: IconProps) => {
  return (
    <svg viewBox="0 0 43 41" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ width: `${width}px`, height: `${height}px` }}>
      <mask id="path-1-inside-1_7553_9324" fill="white">
        <path d="M34.2671 2.73426C34.2797 2.73562 34.2922 2.73715 34.3047 2.73884L34.3306 2.7427C34.3509 2.74588 34.3711 2.74949 34.3912 2.75354C34.4093 2.75684 34.4277 2.7609 34.446 2.76533C34.4613 2.76905 34.4755 2.77272 34.4897 2.7766L34.5165 2.78464C34.5311 2.78897 34.5456 2.79354 34.5601 2.79834C34.6302 2.82146 34.7001 2.8509 34.7684 2.88643L34.6227 2.82034C34.6476 2.82995 34.6722 2.84023 34.6965 2.85118C34.7085 2.8569 34.7213 2.86288 34.734 2.86905L34.7684 2.88643C34.7797 2.89233 34.7909 2.89835 34.8021 2.90451C34.8108 2.90907 34.82 2.91434 34.8292 2.91971L34.8504 2.93236C34.8652 2.94132 34.8798 2.95056 34.8943 2.96007C34.9191 2.9766 34.9424 2.99293 34.965 3.00986C34.9695 3.01338 34.9749 3.01752 34.9804 3.02169C35.0106 3.04498 35.0302 3.06128 35.0495 3.07816C35.0659 3.09261 35.0818 3.10715 35.0973 3.122C35.1037 3.12868 35.1103 3.13515 35.1168 3.14169L35.1311 3.15558C35.1446 3.16948 35.1579 3.1837 35.1709 3.19822C35.184 3.21281 35.1959 3.22662 35.2075 3.24064L35.237 3.27804L35.25 3.2949C35.2953 3.3555 35.3363 3.42052 35.3724 3.48976L35.2884 3.34859C35.3035 3.37095 35.318 3.39371 35.3318 3.41683C35.3344 3.42114 35.3368 3.42507 35.3391 3.42902L35.3509 3.45465L35.3724 3.48976L42.479 17.1186C42.8416 17.814 42.5712 18.6713 41.875 19.0335C41.1787 19.3957 40.3204 19.1255 39.9578 18.4302L34.1115 7.2196L28.2658 18.4302C27.9335 19.0676 27.1845 19.3477 26.5258 19.111L26.3487 19.0335C25.6525 18.6713 25.3821 17.814 25.7447 17.1186L31.7673 5.56522L25.3276 5.56604C24.8921 6.72819 23.9376 7.64311 22.7426 8.05435L22.741 38.1589L29.8479 38.1608C30.5674 38.1608 31.1621 38.6949 31.2562 39.3878L31.2692 39.5805C31.2692 40.3645 30.6329 41.0001 29.8479 41.0001L21.3462 40.9982L21.32 41.0001C21.3104 41.0001 21.3008 41 21.2912 40.9998L12.7921 41.0001C12.0071 41.0001 11.3708 40.3645 11.3708 39.5805C11.3708 38.7964 12.0071 38.1608 12.7921 38.1608L19.8984 38.1589L19.8993 8.05499C18.7034 7.64406 17.7481 6.72879 17.3124 5.56604L10.8702 5.56522L16.8953 17.1186C17.2277 17.756 17.0282 18.5295 16.4564 18.933L16.2913 19.0335C15.5951 19.3957 14.7368 19.1255 14.3742 18.4302L8.52788 7.2196L2.68219 18.4302C2.3498 19.0676 1.60087 19.3477 0.9421 19.111L0.765052 19.0335C0.0688515 18.6713 -0.201582 17.814 0.161023 17.1186L7.26759 3.48976C7.2735 3.47843 7.27953 3.46722 7.2857 3.45613C7.29038 3.44721 7.2956 3.43808 7.30091 3.42902L7.31483 3.40578C7.32662 3.38645 7.33888 3.36738 7.35162 3.34859C7.36147 3.3343 7.37122 3.32044 7.38119 3.30681C7.38828 3.29733 7.39558 3.28763 7.40301 3.27804L7.41927 3.25693C7.43232 3.24067 7.44574 3.22468 7.45954 3.20896C7.47479 3.1917 7.48886 3.17642 7.50321 3.16149C7.50894 3.15604 7.51601 3.14883 7.52315 3.14169L7.54273 3.122C7.5595 3.10591 7.57672 3.09018 7.59438 3.07484C7.60982 3.06135 7.62508 3.04865 7.64058 3.03629C7.64768 3.03101 7.65365 3.02633 7.65965 3.02169L7.67456 3.01017C7.73579 2.96435 7.80155 2.92288 7.87162 2.88643L7.7513 2.95642C7.76328 2.94863 7.77536 2.94103 7.78755 2.93361C7.79507 2.92902 7.80292 2.92433 7.81081 2.91971L7.83618 2.90571L7.87162 2.88643C7.88582 2.87904 7.90008 2.87192 7.91441 2.86506C7.92349 2.86065 7.93303 2.85622 7.94262 2.8519C7.95286 2.84694 7.96386 2.84213 7.97494 2.83745L8.01816 2.8203C8.03772 2.81276 8.05737 2.80568 8.07709 2.79906C8.09167 2.79441 8.10568 2.78998 8.11975 2.78576C8.12946 2.78246 8.13987 2.77947 8.15033 2.7766L8.19172 2.76589C8.21267 2.76078 8.23368 2.75616 8.25473 2.75203C8.27152 2.74905 8.28858 2.74602 8.30569 2.74329C8.37738 2.73186 8.45208 2.72588 8.52818 2.72588L8.38481 2.73296C8.38733 2.73271 8.38986 2.73246 8.39238 2.73221C8.40377 2.73092 8.41453 2.73002 8.42528 2.72925C8.4523 2.72741 8.48008 2.72617 8.50793 2.72575L8.51248 2.72567L8.52818 2.72588L17.3117 2.72692C17.909 1.1305 19.4855 0.00012207 21.32 0.00012207C23.1545 0.00012207 24.731 1.1305 25.3283 2.72692L34.1118 2.72588L34.134 2.72578C34.1599 2.72621 34.1858 2.72735 34.2116 2.72918C34.216 2.72933 34.221 2.72971 34.2261 2.73011L34.2671 2.73426ZM15.6347 21.8062C16.4197 21.8062 17.0561 22.4418 17.0561 23.2259C17.0561 27.7867 13.2253 31.46 8.52818 31.46C3.83104 31.46 0.000292403 27.7867 0.000292403 23.2259C0.000292403 22.4418 0.636636 21.8062 1.42161 21.8062H15.6347ZM41.2184 21.8062C42.0034 21.8062 42.6397 22.4418 42.6397 23.2259C42.6397 27.7867 38.809 31.46 34.1118 31.46C29.4147 31.46 25.5839 27.7867 25.5839 23.2259C25.5839 22.4418 26.2203 21.8062 27.0053 21.8062H41.2184ZM14.0141 24.6456H3.04228C3.69803 26.9292 5.89725 28.6206 8.52818 28.6206C11.0395 28.6206 13.1575 27.0795 13.9152 24.9532L14.0141 24.6456ZM39.5977 24.6456H28.6259C29.2817 26.9292 31.4809 28.6206 34.1118 28.6206C36.6232 28.6206 38.7411 27.0795 39.4988 24.9532L39.5977 24.6456ZM21.32 2.83946C20.5223 2.83946 19.8987 3.43747 19.8987 4.14555C19.8987 4.85363 20.5223 5.45165 21.32 5.45165C22.1177 5.45165 22.7413 4.85363 22.7413 4.14555C22.7413 3.43747 22.1177 2.83946 21.32 2.83946Z" />
      </mask>
      <path
        d="M34.2671 2.73426C34.2797 2.73562 34.2922 2.73715 34.3047 2.73884L34.3306 2.7427C34.3509 2.74588 34.3711 2.74949 34.3912 2.75354C34.4093 2.75684 34.4277 2.7609 34.446 2.76533C34.4613 2.76905 34.4755 2.77272 34.4897 2.7766L34.5165 2.78464C34.5311 2.78897 34.5456 2.79354 34.5601 2.79834C34.6302 2.82146 34.7001 2.8509 34.7684 2.88643L34.6227 2.82034C34.6476 2.82995 34.6722 2.84023 34.6965 2.85118C34.7085 2.8569 34.7213 2.86288 34.734 2.86905L34.7684 2.88643C34.7797 2.89233 34.7909 2.89835 34.8021 2.90451C34.8108 2.90907 34.82 2.91434 34.8292 2.91971L34.8504 2.93236C34.8652 2.94132 34.8798 2.95056 34.8943 2.96007C34.9191 2.9766 34.9424 2.99293 34.965 3.00986C34.9695 3.01338 34.9749 3.01752 34.9804 3.02169C35.0106 3.04498 35.0302 3.06128 35.0495 3.07816C35.0659 3.09261 35.0818 3.10715 35.0973 3.122C35.1037 3.12868 35.1103 3.13515 35.1168 3.14169L35.1311 3.15558C35.1446 3.16948 35.1579 3.1837 35.1709 3.19822C35.184 3.21281 35.1959 3.22662 35.2075 3.24064L35.237 3.27804L35.25 3.2949C35.2953 3.3555 35.3363 3.42052 35.3724 3.48976L35.2884 3.34859C35.3035 3.37095 35.318 3.39371 35.3318 3.41683C35.3344 3.42114 35.3368 3.42507 35.3391 3.42902L35.3509 3.45465L35.3724 3.48976L42.479 17.1186C42.8416 17.814 42.5712 18.6713 41.875 19.0335C41.1787 19.3957 40.3204 19.1255 39.9578 18.4302L34.1115 7.2196L28.2658 18.4302C27.9335 19.0676 27.1845 19.3477 26.5258 19.111L26.3487 19.0335C25.6525 18.6713 25.3821 17.814 25.7447 17.1186L31.7673 5.56522L25.3276 5.56604C24.8921 6.72819 23.9376 7.64311 22.7426 8.05435L22.741 38.1589L29.8479 38.1608C30.5674 38.1608 31.1621 38.6949 31.2562 39.3878L31.2692 39.5805C31.2692 40.3645 30.6329 41.0001 29.8479 41.0001L21.3462 40.9982L21.32 41.0001C21.3104 41.0001 21.3008 41 21.2912 40.9998L12.7921 41.0001C12.0071 41.0001 11.3708 40.3645 11.3708 39.5805C11.3708 38.7964 12.0071 38.1608 12.7921 38.1608L19.8984 38.1589L19.8993 8.05499C18.7034 7.64406 17.7481 6.72879 17.3124 5.56604L10.8702 5.56522L16.8953 17.1186C17.2277 17.756 17.0282 18.5295 16.4564 18.933L16.2913 19.0335C15.5951 19.3957 14.7368 19.1255 14.3742 18.4302L8.52788 7.2196L2.68219 18.4302C2.3498 19.0676 1.60087 19.3477 0.9421 19.111L0.765052 19.0335C0.0688515 18.6713 -0.201582 17.814 0.161023 17.1186L7.26759 3.48976C7.2735 3.47843 7.27953 3.46722 7.2857 3.45613C7.29038 3.44721 7.2956 3.43808 7.30091 3.42902L7.31483 3.40578C7.32662 3.38645 7.33888 3.36738 7.35162 3.34859C7.36147 3.3343 7.37122 3.32044 7.38119 3.30681C7.38828 3.29733 7.39558 3.28763 7.40301 3.27804L7.41927 3.25693C7.43232 3.24067 7.44574 3.22468 7.45954 3.20896C7.47479 3.1917 7.48886 3.17642 7.50321 3.16149C7.50894 3.15604 7.51601 3.14883 7.52315 3.14169L7.54273 3.122C7.5595 3.10591 7.57672 3.09018 7.59438 3.07484C7.60982 3.06135 7.62508 3.04865 7.64058 3.03629C7.64768 3.03101 7.65365 3.02633 7.65965 3.02169L7.67456 3.01017C7.73579 2.96435 7.80155 2.92288 7.87162 2.88643L7.7513 2.95642C7.76328 2.94863 7.77536 2.94103 7.78755 2.93361C7.79507 2.92902 7.80292 2.92433 7.81081 2.91971L7.83618 2.90571L7.87162 2.88643C7.88582 2.87904 7.90008 2.87192 7.91441 2.86506C7.92349 2.86065 7.93303 2.85622 7.94262 2.8519C7.95286 2.84694 7.96386 2.84213 7.97494 2.83745L8.01816 2.8203C8.03772 2.81276 8.05737 2.80568 8.07709 2.79906C8.09167 2.79441 8.10568 2.78998 8.11975 2.78576C8.12946 2.78246 8.13987 2.77947 8.15033 2.7766L8.19172 2.76589C8.21267 2.76078 8.23368 2.75616 8.25473 2.75203C8.27152 2.74905 8.28858 2.74602 8.30569 2.74329C8.37738 2.73186 8.45208 2.72588 8.52818 2.72588L8.38481 2.73296C8.38733 2.73271 8.38986 2.73246 8.39238 2.73221C8.40377 2.73092 8.41453 2.73002 8.42528 2.72925C8.4523 2.72741 8.48008 2.72617 8.50793 2.72575L8.51248 2.72567L8.52818 2.72588L17.3117 2.72692C17.909 1.1305 19.4855 0.00012207 21.32 0.00012207C23.1545 0.00012207 24.731 1.1305 25.3283 2.72692L34.1118 2.72588L34.134 2.72578C34.1599 2.72621 34.1858 2.72735 34.2116 2.72918C34.216 2.72933 34.221 2.72971 34.2261 2.73011L34.2671 2.73426ZM15.6347 21.8062C16.4197 21.8062 17.0561 22.4418 17.0561 23.2259C17.0561 27.7867 13.2253 31.46 8.52818 31.46C3.83104 31.46 0.000292403 27.7867 0.000292403 23.2259C0.000292403 22.4418 0.636636 21.8062 1.42161 21.8062H15.6347ZM41.2184 21.8062C42.0034 21.8062 42.6397 22.4418 42.6397 23.2259C42.6397 27.7867 38.809 31.46 34.1118 31.46C29.4147 31.46 25.5839 27.7867 25.5839 23.2259C25.5839 22.4418 26.2203 21.8062 27.0053 21.8062H41.2184ZM14.0141 24.6456H3.04228C3.69803 26.9292 5.89725 28.6206 8.52818 28.6206C11.0395 28.6206 13.1575 27.0795 13.9152 24.9532L14.0141 24.6456ZM39.5977 24.6456H28.6259C29.2817 26.9292 31.4809 28.6206 34.1118 28.6206C36.6232 28.6206 38.7411 27.0795 39.4988 24.9532L39.5977 24.6456ZM21.32 2.83946C20.5223 2.83946 19.8987 3.43747 19.8987 4.14555C19.8987 4.85363 20.5223 5.45165 21.32 5.45165C22.1177 5.45165 22.7413 4.85363 22.7413 4.14555C22.7413 3.43747 22.1177 2.83946 21.32 2.83946Z"
        fill="none"
        stroke={color}
        strokeWidth="4"
        mask="url(#path-1-inside-1_7553_9324)"
      />
    </svg>
  );
};

export const TargetIcon = ({ height = "32", width = "32", color = "currentColor" }: IconProps) => {
  return (
    <svg viewBox="0 0 40 44" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ width: `${width}px`, height: `${height}px` }}>
      <path
        d="M1.55741 15.3513C4.87956 7.24452 12.8631 2.3322 21.2664 3.22433C22.0243 3.30479 22.5762 4.0114 22.4991 4.80259C22.4221 5.59377 21.7452 6.16992 20.9873 6.08946C13.7845 5.32478 6.9414 9.53534 4.09385 16.484C1.24629 23.4327 3.05507 31.5069 8.55917 36.4168C14.0633 41.3267 21.9854 41.9327 28.1163 37.913C34.2473 33.8932 37.1644 26.1805 35.3177 18.8727C35.1234 18.1038 35.563 17.3159 36.2996 17.1131C37.0362 16.9102 37.7909 17.3692 37.9852 18.1381C40.1397 26.6639 36.7365 35.6621 29.5836 40.3518C22.4308 45.0415 13.1884 44.3344 6.76695 38.6062C0.345502 32.8781 -1.76475 23.4581 1.55741 15.3513ZM19.3015 11.7607C20.0633 11.7602 20.6813 12.4044 20.6817 13.1997C20.6822 13.995 20.0651 14.6401 19.3032 14.6406C15.7715 14.643 12.6302 16.9841 11.4809 20.4702C10.3317 23.9563 11.4277 27.8197 14.2101 30.0904C16.9925 32.361 20.8485 32.5389 23.8119 30.5333C26.7753 28.5278 28.1935 24.7804 27.3434 21.202C27.16 20.4302 27.6108 19.6492 28.3502 19.4578C29.0896 19.2664 29.8377 19.7369 30.0211 20.5088C31.1545 25.2797 29.2637 30.2759 25.3126 32.9498C21.3616 35.6238 16.2206 35.3866 12.511 32.3592C8.80133 29.3318 7.34008 24.181 8.87231 19.5331C10.4045 14.8852 14.5928 11.7639 19.3015 11.7607ZM34.2249 1.41042L34.9722 5.48828L38.8786 6.26842C39.9605 6.48448 40.3753 7.87191 39.6032 8.69203L33.7325 14.928C33.5232 15.1503 33.2505 15.2957 32.9553 15.3424L26.5064 16.3615L19.1632 24.0278C18.6735 24.539 17.9071 24.5855 17.3671 24.1672L17.2124 24.0278C16.6737 23.4655 16.6737 22.5537 17.2124 21.9914L24.555 14.3244L25.5325 7.59379C25.5772 7.28561 25.7165 7.0009 25.9295 6.78242L31.9032 0.653973C32.6888 -0.152008 34.0179 0.281028 34.2249 1.41042ZM31.9994 4.59318L28.1913 8.49987L27.4959 13.2929L32.0873 12.5669L35.8297 8.59166L33.5341 8.13322C32.9789 8.02234 32.5447 7.56906 32.4385 6.98948L31.9994 4.59318Z"
        fill={color}
      />
    </svg>
  );
};
