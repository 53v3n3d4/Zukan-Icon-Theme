// example from https://www.typescriptlang.org/docs/handbook/2/modules.html

function loggingIdentity<Type>(arg: Type[]): Type[] {
  console.log(arg.length);
  return arg;
}

class Point {
  x: number;
  y: number;
}
 
const pt = new Point();
pt.x = 0;
pt.y = 0;

// @filename: hello.ts
export default function helloWorld() {
  console.log("Hello, world!");
}

import helloWorld from "./hello.js";
helloWorld();

// @filename: maths.ts
export var pi = 3.14;
export let squareTwo = 1.41;
export const phi = 1.61;
 
export class RandomNumberGenerator {}
 
export function absolute(num: number) {
  if (num < 0) return num * -1;
  return num;
}

// @filename: animal.ts
export type Cat = { breed: string; yearOfBirth: number };
 
export interface Dog {
  breeds: string[];
  yearOfBirth: number;
}
 
// @filename: app.ts
import { Cat, Dog } from "./animal.js";
type Animals = Cat | Dog;

export type OrgParams = {
  name: string;
  billingAddress: string;
  baseRepoRole: string;
};

type Props = { notice: Notice; clear: () => void };

import { RoleAssignment } from './RoleAssignment';
import type { RoleAssignmentParams } from './RoleAssignment';

export { Issue, Org, Repo, Role, User, UserContext, RoleAssignment };
export type { LoggedInUser, OrgParams, RoleAssignmentParams };

import type { Meta, StoryObj } from 'storybook-solidjs';

import { Button } from './Button';

const meta: Meta<typeof Button> = {
  component: Button,
};

export default meta;
type Story = StoryObj<typeof Button>;

/*
 *👇 Render functions are a framework specific feature to allow you control on how the component renders.
 * See https://storybook.js.org/docs/api/csf
 * to learn how to use render functions.
 */
export const Primary: Story = {
  render: () => <Button primary label="Button" />,
};
