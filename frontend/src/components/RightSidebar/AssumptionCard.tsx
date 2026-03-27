import React from 'react';
import { Lightbulb, ArrowRight } from 'lucide-react';
import { Assumption } from '@/types';
import { useAppStore } from '@/store';

interface AssumptionCardProps {
  assumption: Assumption;
  assumptionId?: string;
}

const AssumptionCard: React.FC<AssumptionCardProps> = ({ assumption, assumptionId }) => {
  const { selectAssumption } = useAppStore();

  const confidenceColor = 
    assumption.confidence >= 0.8 ? 'text-green-500' :
    assumption.confidence >= 0.5 ? 'text-orange-500' : 
    'text-red-500';

  return (
    <div className="bg-dark-light border border-dark-border rounded p-3">
      <div className="flex items-start gap-2 mb-2 min-w-0">
        <Lightbulb size={16} className="text-yellow-500 shrink-0 mt-0.5" />
        <div className="text-sm text-text-primary leading-snug min-w-0 break-words">
          {assumption.text}
        </div>
      </div>

      <div className="flex items-center justify-between text-xs mt-3 pt-2 border-t border-dark-border">
        <div className="flex items-center gap-1.5">
          <span className="text-text-muted">Confidence:</span>
          <span className={`font-bold ${confidenceColor}`}>
            {Math.round(assumption.confidence * 100)}%
          </span>
        </div>

        {assumptionId && (
          <button
            onClick={() => selectAssumption(assumptionId)}
            className="flex items-center gap-1 text-accent-textual hover:text-blue-400 transition-colors"
          >
            <span>Go to assumption</span>
            <ArrowRight size={10} />
          </button>
        )}
      </div>
    </div>
  );
};

export default AssumptionCard;
