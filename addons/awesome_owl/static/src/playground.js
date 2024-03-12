/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
        this.value1 = "<div class='text-primary'>some text 1</div>";
        this.value2 = markup("<div class='text-primary'>some text 2</div>");
    }

}
