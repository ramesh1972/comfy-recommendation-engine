
import { 
  Accordion, 
  AccordionContent, 
  AccordionItem, 
  AccordionTrigger 
} from "@/components/ui/accordion";
import { Card } from "@/components/ui/card";

const ExplanationSection = () => {
  return (
    <Card className="p-6">
      <h2 className="text-2xl font-bold mb-4">How It Works</h2>
      <Accordion type="single" collapsible className="w-full">
        <AccordionItem value="item-1">
          <AccordionTrigger>What is Collaborative Filtering?</AccordionTrigger>
          <AccordionContent>
            <p className="text-muted-foreground">
              Collaborative filtering is a technique used by recommender systems to make automatic predictions about the interests of a user by collecting preferences from many users. It works on the assumption that if person A has the same opinion as person B on an item, A is more likely to have B's opinion on a different item.
            </p>
          </AccordionContent>
        </AccordionItem>
        
        <AccordionItem value="item-2">
          <AccordionTrigger>How does this demo work?</AccordionTrigger>
          <AccordionContent>
            <p className="text-muted-foreground">
              This demo uses a FastAPI backend that loads a pre-trained recommendation model from a pickle file. The model was created using user ratings data and collaborative filtering techniques. When you select a user, the system queries the model to find products that similar users have enjoyed and recommends them to you.
            </p>
          </AccordionContent>
        </AccordionItem>
        
        <AccordionItem value="item-3">
          <AccordionTrigger>Can I rate products?</AccordionTrigger>
          <AccordionContent>
            <p className="text-muted-foreground">
              Yes! You can rate products and your ratings will be sent to the backend. In a production system, these new ratings would be used to periodically retrain the model, improving recommendations over time. For this demo, your ratings are collected but don't immediately affect the recommendations.
            </p>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </Card>
  );
};

export default ExplanationSection;
