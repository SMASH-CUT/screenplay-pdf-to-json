export interface ILineParse {
  text: string;
  x: number;
  y: number;
  height: number;
  width: number;
}

export interface IFinalParse {
  page: number;
  content: ILineParse[];
}
